import asyncio
import threading
import time

import pika
import pytz
from sqlalchemy import text
from urllib.parse import urlparse
from datetime import datetime, timedelta

from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.cli_command import CLICommand
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.console import CommandHandler
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.migrate import run_migrations
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.predef import CUSTOM_HEADER, GLOBAL_TIMEZONE, MAX_DIRECT_HTTP, USER_AGENT_NAME
import CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.rds as rds
import CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.local as local_rds
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.util import thlog
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.crawing import fetch_with_redirects, socket_fetch_with_redirects
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.mime import get_mime_type_from_binary
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.parser.html import HTMLSimpleParser
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.parser.json import parse_json_string
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.parser.robots import check_robot_permission_from_rules, fetch_robots_txt
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.parser.uri import normalize_uri_path
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.parser.xml import  extract_links_from_xml
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.string import shorten_string
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.stringify.json import stringify_to_json
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.abstract.rds.predef import DatabaseType
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.connection_info import Connection_Info
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.pika_rabbitmq import PikaRabbitMQ
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.scrapper_root import Scrapper_Root
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.sqlalchemy import SQLAlchemyConnection
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.thread_manager import ThreadManager
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.scrapper_root_access_rule import Scrapper_Root_Access_Rule
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.db.models import *
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.thread_worker import WorkerThread
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.udp_client import UDPClient
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.udp_server import UDPServer
from .import_path import add_module_path





def start_threaded_callback(name: str, mq_session: PikaRabbitMQ | list[PikaRabbitMQ], console: CommandHandler, thread_manager: ThreadManager, dependency_thread: WorkerThread | None, callback, interval_sec):
    """Start the callback in a new thread with the ability to stop it."""
    
    def schedule_callback(callback, interval_sec, stop_event):
        """Schedules a callback to be executed at regular intervals."""
        async def periodic_execution():
            loop = asyncio.get_event_loop()
            while not stop_event.is_set():  # stop_event가 set되면 종료
                try:
                    await callback(dependency_thread, name, mq_session, console, thread_manager, stop_event)
                except Exception as e:
                    # print(f"Scheduled callback error: {e}")
                    pass
                    
                await asyncio.sleep(interval_sec)

            loop.stop()  # 이벤트 루프 종료

        loop = asyncio.new_event_loop()  # 새로운 이벤트 루프 생성
        asyncio.set_event_loop(loop)  # 현재 스레드의 이벤트 루프 설정

        loop.create_task(periodic_execution())  # 주기적인 콜백 실행
        loop.run_forever()  # 이벤트 루프 실행 (이 스레드가 계속 실행되도록 함)
    
    stop_event = asyncio.Event()  # 종료 신호를 보내기 위한 이벤트
    
    def run_schedule():
        schedule_callback(callback, interval_sec, stop_event)
        
    # 새로운 스레드에서 실행
    thread = threading.Thread(target=run_schedule, name=f'_ingot_taskkill_manage_thread__{name}', daemon=True)
    thread.start()  # 새로운 스레드 시작

    return stop_event, thread  # stop_event와 thread 반환



async def _inthread_dying_check(this_thread: WorkerThread | None, rootkey: str, mq_session: PikaRabbitMQ, console: CommandHandler, thread_manager: ThreadManager, event: asyncio.Event):
    
    cnt = thread_manager.get_active_worker_count()
    # length = len(thread_manager.worker_threads)
    


    if this_thread != None and console.running == False:
        
        # thlog(rootkey, f"[sub] Thread manager has {cnt}/{length} workers. Stopping all.")

        if cnt == 0:
            event.set()
            return


        if mq_session._closed_flag:
            #consume 동작 중 큐 소비를 하기 위한 대기만 반복되는 경우. 강제로 벗어나기 위해 연결을 해제한다.
            if mq_session.force_channel_consuming_stop():
                mq_session.init(is_shutdown_init=True)
                thlog(rootkey, "Message queue channel closed.")

        if this_thread in thread_manager.worker_threads:
            this_thread.stop()
            event.set()
                

async def _mainthread_dying_check(this_thread: WorkerThread | None, rootkey: str, mq_session: list[PikaRabbitMQ], console: CommandHandler, thread_manager: ThreadManager, event: asyncio.Event):
    if console.running == False:
        cnt = thread_manager.get_active_worker_count()
        length = len(thread_manager.worker_threads)
        
        thlog(rootkey, f"Thread manager has {cnt}/{length} workers. Waiting for all threads to finish... \nall ongoing operations will complete before termination. If any operation is in progress, it may take some time to fully shut down.")
        
        if cnt != 0:
            for worker in thread_manager.worker_threads:
                if worker.is_alive():
                    worker.stop()
                    # thlog(rootkey, f"Thread {worker.name} stopped.")
            
        if cnt == 0:
            event.set()
            
        return



def _worker_start_ingot(root: Roots, db_session: SQLAlchemyConnection, mq_session: PikaRabbitMQ, console: CommandHandler, ):
    """워커 연결용 함수.
    Args:
        root (Scrapper_Root): root 정보가 포함된 데이터
        db_session (SQLAlchemyConnection): rds 요청용 데이터베이스 세션
        mq_session (PikaRabbitMQ): 메세지 큐를 요청하거나 소비하기 위한 세션
    """
    
    thlog(root.root_key, f"worker start")
    

    if not mq_session._chk_usable():
        thlog(root.root_key, f"MQ connection is not usable.")
    
    if mq_session._channel.is_closed:
        thlog(root.root_key, f"MQ channel is closed. so reconnect")
        connected = mq_session.reconnect()
        if connected:
            mq_session.declare_channel()
            thlog(root.root_key, f"MQ channel reconnected.")
        else:
            thlog(root.root_key, f"MQ channel reconnect failed.")
            return

    config = {
        'exchange_name': f'{root.root_key}.exchange',
        'queue_name': f'{root.root_key}.queue',
        'route_key': f'{root.root_key}.direct_route'
    }

    
    # rules object 생성
    rules: Scrapper_Root_Access_Rule = Scrapper_Root_Access_Rule()
    rules.put_json(parse_json_string(root.rules))


    mq_session.declare_exchange(config['exchange_name'], 'direct', durable=True, )
    mq_session.declare_queue(config['queue_name'], durable=True)
    mq_session.bind_queue(config['exchange_name'], config['queue_name'], config['route_key'])
    
    
    async def crawling_and_queuing(id: int | None, uri: str):
        
        if console.running == False:
            return
            
        try:
            uri_data = urlparse(uri)
            base_url = f"{uri_data.scheme}://{uri_data.hostname}"
            time_zone = pytz.timezone(GLOBAL_TIMEZONE)
            nowtime = datetime.now(time_zone)
            
            
            
            ## robots.txt 체크
            robot_ok = False
            with db_session.get_db() as db:
                robot = rds.get_robots_by_domain(db, base_url)
                
                
                
                if robot != None:

                    # 로봇의 updated_at이 한국 시간으로 저장된 경우
                    last_time = robot.updated_at
                    # updated_at을 UTC로 변환
                    # last_time_utc = last_time.astimezone(pytz.utc)

                    # 현재 시간 (nowtime)이 한국 시간으로 되어 있다면 UTC로 변환
                    nowtime_utc = nowtime.astimezone(pytz.utc)

                    last_time = pytz.utc.localize(last_time)

                    # 시간 차이 계산
                    time_difference = nowtime_utc - last_time
                    
                    

                    robot_ruleset = robot.ruleset_text
                    
                    if isinstance(time_difference, timedelta) and time_difference > rules.robots_txt_expiration_time:
                        # print('로봇체크 캐시 업데이트 시작')
                        robot_ruleset = await fetch_robots_txt(uri)
                        rds.update_robot(db, base_url, robot_ruleset, GLOBAL_TIMEZONE)
                        thlog(root.root_key, f"Cache robots.txt rule updated", time_difference, base_url)
                        # print('로봇체크 캐시 업데이트 종료')
                        
                    # print('로봇체크 캐시로 시작')
                    robot_ok = check_robot_permission_from_rules(USER_AGENT_NAME, robot_ruleset, uri)
                    # print('로봇체크 캐시로 종료')
                    thlog(root.root_key, f"Cache robots.txt rule check")
                    
                else:
                    robot_ruleset = await fetch_robots_txt(uri)
                    rds.update_robot(db, base_url, robot_ruleset, GLOBAL_TIMEZONE)
                    robot_ok = check_robot_permission_from_rules(USER_AGENT_NAME, robot_ruleset, uri)
                    thlog(root.root_key, f"Live robots.txt rule check", base_url)

            if not robot_ok:
                thlog(root.root_key, f"robots.txt check failed: {base_url}")
                return
    


            try:
                
                final_response = socket_fetch_with_redirects(uri, max_redirects=MAX_DIRECT_HTTP, headers=CUSTOM_HEADER)

                status_code = final_response['status_code']
                # http_body = final_response['body']
                
                # 에러가 400대 이상인 경우는 정상적이지 않음.. 그래서 넘기는거임
                if status_code >= 400:
                    thlog(root.root_key, f"Failed with status code: {status_code}")
                    return


                links = extract_links_from_xml(final_response['body'])
                link_length = len(links)
                
                thlog(root.root_key, f"Links count: {link_length} from id : {id}")

                idx = 0
                for link in links:
                    idx += 1
                    link['id'] = id
                    mq_session.b_publish(config['exchange_name'], config['route_key'], stringify_to_json(link)) 
                    
                    if console.running == False:
                        thlog(root.root_key, f"Console has shut down and delays have disappeared in the progress of the scheduled upload queue. {idx}/{link_length}")
                    else:
                        time.sleep(rules.queue_upload_delay_seconds)
    
                
            except Exception as e:
                thlog(root.root_key, e)


            
                
        except ValueError as ve:
            thlog(root.root_key, 'crawling value error - ', ve)
        except Exception as e:
            thlog(root.root_key, 'crawling except - ',e)





    if console.running == False:
        return

    # 루트에 브렌치 데이터가 없으면 크롤링 요청
    flag_branch_no_exists = False 
    with db_session.get_db() as db:
        cnt = rds.get_root_branch_count(db, root.id)
        if cnt == 0:
            flag_branch_no_exists = True
    

    # 최초에 브렌치 데이터 없으면 요청해서 메세지 큐를 생성. 
    if flag_branch_no_exists:
        try:
            asyncio.run(crawling_and_queuing(None, root.root_uri))
            thlog(root.root_key, f"first branch creation done")
        except Exception as e:
            thlog(root.root_key, f"root init crawling error", e)
        
    
    
           
    
 
        
    # 메세지 큐 소비 처리
    def callback(ch: pika.channel.Channel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes):
        
        if console.running == False:
            return
        
        obj = parse_json_string(body)
        
        parent_id = obj['id']
        
        thlog(root.root_key, f"Queue received: parent_id: {parent_id}, uri:{shorten_string(obj['url'], 40)}, relative:{obj['is_relative']}")
        
        
        # 브랜치 등록 체크
        def dup_chk(root_id: int, uri: str) -> (int | None):
            with db_session.get_db() as db:
                return rds.get_branch_id_if_exists(db, root_id, uri)


        # 브렌치가 존재하면 브랜치 생성
        def branch_up(id: int | None, uri: str) -> (int | None):
            with db_session.get_db() as db:
                branch = Branches()
                branch.id = None
                branch.parent_id = id
                branch.root_id = root.id
                branch.branch_uri = uri
                ids = rds.update_branches(db, branches=[branch])
                if ids:
                    return ids[0]
                return None


        # 브렌치가 존재하지 않으면 새로 생성
        async def leaf_up(id: int | None, uri: str) -> (int | None):
            
            try:
                    
                final_response = fetch_with_redirects(uri, max_redirects=MAX_DIRECT_HTTP, headers=CUSTOM_HEADER)
                
                content_type = final_response['content_type']
                http_body = final_response['body']
                mime = get_mime_type_from_binary(http_body.encode() if isinstance(http_body, str) else http_body)
                
                if isinstance(http_body, bytes):
                    mime = get_mime_type_from_binary(http_body)
                else:
                    mime = get_mime_type_from_binary(http_body.encode())

                if mime == "application/octet-stream" and content_type != mime:
                    mime = content_type
                        
                html_parser = HTMLSimpleParser(html_string=http_body)   
                
                with db_session.get_db() as db:
                    leaf = Leaves()
                    leaf.id = None
                    leaf.root_id = root.id
                    leaf.branch_id = id
                    # leaf.val_classified = 'none-test'
                    leaf.val_mime_type = mime
                    
                    if mime == 'text/html':
                        leaf.val_html_meta_author = html_parser.extract_meta_author()
                        leaf.val_html_meta_description = html_parser.extract_meta_description()
                        leaf.val_html_meta_keywords = html_parser.extract_meta_keywords()
                        leaf.val_html_meta_title = html_parser.extract_title_tags()
                        leaf.val_html_meta_og_title = html_parser.extract_og_meta_tags('title')
                        leaf.val_main_language = html_parser.extract_html_lang()
                    
                    
                    ids = rds.update_leaves(db, leaves=[leaf])
                    if ids:
                        return ids[0]
                    return None
            except Exception as e:
                thlog(root.root_key, f"leaf_up error: {e}")
                return None
            
            

        try:
            if obj['is_relative']:
                # 상대경로
                parsed_url = urlparse(root.root_uri)
                assembled_uri_with_path = parsed_url.scheme+'://' + normalize_uri_path(f"{parsed_url.netloc}{parsed_url.path}{obj['url']}")
                assembled_uri_no_path = parsed_url.scheme+'://' + normalize_uri_path(f"{parsed_url.netloc}{obj['url']}")
                
                d1 = dup_chk(root.id, assembled_uri_with_path)
                d2 = dup_chk(root.id, assembled_uri_no_path)
                
                
                if d1 == None:
                    id = branch_up(parent_id, assembled_uri_with_path)
                    # print(f"branch id: {parent_id} / {id}")
                    if not id == None:
                        asyncio.run(crawling_and_queuing(id, assembled_uri_with_path))
                        asyncio.run(leaf_up(id, assembled_uri_with_path))
                else:
                    rds.increment_branch_duplicated_count(db, d1)
                    
                if d2 == None:
                    id = branch_up(parent_id, assembled_uri_no_path)
                    # print(f"branch id: {parent_id} / {id}")
                    if not id == None:
                        asyncio.run(crawling_and_queuing(id, assembled_uri_no_path))
                        asyncio.run(leaf_up(id, assembled_uri_no_path))
                else:
                    rds.increment_branch_duplicated_count(db, d2)
            else:
                # 절대경로
                assembled_uri = obj['url']
                
                dd = dup_chk(root.id, assembled_uri)
                if not dd:
                    id = branch_up(parent_id, assembled_uri)
                                        
                    # print(f"branch id: {parent_id} / {id}")
                    if not id == None:
                        
                        asyncio.run(crawling_and_queuing(id, assembled_uri))
                        asyncio.run(leaf_up(id, assembled_uri))
                else:
                    rds.increment_branch_duplicated_count(db, dd)
                        
                
                
                
        except Exception as e:
            # import traceback
            # error_details = traceback.format_exc()
            thlog(root.root_key, f"Queue processing error: {e}")
        




    thlog(root.root_key, f'start consuming')
    # 메세지 큐 소비
    # mq_session.set_qos(1)
    mq_session.b_consume(config['queue_name'], callback, delay_sec=rules.consume_delay_seconds,)
    # 쓰레드 종료 메세지
    thlog(root.root_key, f"worker process complete")
    
    
    











def initialize(
    db_rds_connection: Connection_Info, # db storage connection info
    db_mq_connection: Connection_Info, # db storage connection info
    roots: list[Scrapper_Root] # root list
    ):
    """
    프로그램 시작점
    """
    
    add_module_path("../")
    
    # 메인 쓰레드가 콘솔 명을을 기다리며 대기한다
    console: CommandHandler = CommandHandler()
    
    print("hello")
    
    conn = SQLAlchemyConnection()
    conn.connection = db_rds_connection
    

    profile_connection = Connection_Info()
    profile_connection.db_type = DatabaseType.SQLITE3
    profile_connection.database = "_local_config.db"

    local = SQLAlchemyConnection()
    local.connection = profile_connection
    
    

    
    # 로컬 데이터에 접근
    with local.get_db() as db:
        local_rds.table_init(local._engine, db, profile_connection.db_type)

    
    
    # 공용 데이터에 접근
    all_roots: list[Roots] = []
    with conn.get_db() as db:
        # rds db table init
        rds.table_init(conn._engine, db, db_rds_connection.db_type) # 테이블 생성
        rds.update_roots(db, roots) # root 정보 업데이트



        # 모든 root를 획득.
        page_n: int = 1
        while True:
            new_roots = rds.get_roots_list(db, page_n)
            if not new_roots:
                break
            all_roots.extend(new_roots)
            page_n += 1
        
    
    
    thread_manager = ThreadManager()
    thread_manager.add_watcher(check_interval=4)
    
    all_mq_session: list[PikaRabbitMQ] = []
    
    #test
    all_roots = []
    
    for i, root in enumerate(all_roots):
        # 메시지 큐 연결
        mq_conn = PikaRabbitMQ(root.root_key)
        is_conn = mq_conn.connect(db_mq_connection.host, db_mq_connection.port, db_mq_connection.user, db_mq_connection.password, db_mq_connection.vhost)
        if not is_conn:
            print(f"Failed to connect to RabbitMQ server for root {root.root_key}.")
            continue
        
        # 채널 생성
        mq_conn.declare_channel()
        
        # 전역 관리를 위한 메세지 큐 세션 추가
        all_mq_session.append(mq_conn)
        

        # 하위 일꾼 쓰레드
        worker = thread_manager.add_worker(name=root.root_key, target=_worker_start_ingot, args=(root, conn, mq_conn, console, ), thread_id=i)
        
        # 하위 쓰레드 사망 시 감지해서 트리거하는 쓰레드
        start_threaded_callback(root.root_key, mq_conn, console, thread_manager, worker, _inthread_dying_check, 10)
            
        
    # 전역에서 하위 쓰레드 죽으면 감지해서 계속 죽이는 쓰레드
    start_threaded_callback('main', all_mq_session, console, thread_manager, None, _mainthread_dying_check, 30)
    
    # 하위 쓰레드 실행
    thread_manager.start_all()
    
    ###=======================================
    ### db 마이그레이션
    ###======================================= 
    # _build_connection_url() 메소드를 사용해 마이그레이션 한다.
    # initialize_branch("main", conn._build_connection_url())
    # initialize_branch("local", local._build_connection_url())
    
    # conn_url = conn._build_connection_url()
    # local_url = local._build_connection_url()
    
    # if has_no_migrations("main", conn_url):
    #     run_migrations("main", conn_url, 'revision')
    #     print("----------1")
        
    # if has_no_migrations("local", local_url):
    #     run_migrations("local", local_url, 'revision')
    #     print("----------2")
    
    # if is_up_to_date("main", conn_url):
    #     run_migrations("main", conn_url, 'upgrade')
    #     print("----------3")
    
    # if is_up_to_date("local", conn_url): 
    #     run_migrations("local", local_url, 'upgrade')
    #     print("----------4")
    
    # run_migrations("main", conn_url, 'upgrade', version_url=local_url)
    # run_migrations("local", local_url, 'upgrade', version_url=local_url)
    
    
    ###=======================================
    ### 기능 초기화
    ###======================================= 
    # 마스터노드용 서버 
    # 동작은 cli에 의존함
    service_mesh_master: UDPServer = UDPServer()
    
    # 슬레이브 노드용 서버
    # (상동함)
    service_mesh_slave: UDPClient = UDPClient('localhost', 12345)
    
    
    ###=======================================
    ### 메인쓰레드용 명령어 콘솔 프로그램
    ### - 명령어를 명시적으로 생성자를 통해 등록함.
    ### - 타입을 위해 dict 안 씀. 타입에 찌들어서 이런게 가끔 역겨움. 그냥 강제했으면 좋겠다
    ###======================================= 
    cli_commands: CLICommand = CLICommand(  console, 
                                            all_roots, 
                                            all_mq_session, 
                                            conn, local, 
                                            service_mesh_master, 
                                            service_mesh_slave, 
                                            run_migrations )

    data_local_guild_is = False
    data_local_unique_id = ''
    data_local_guild_token = ''
    data_local_address_outer_ip = ''
    data_local_address_inner_ip = ''
    data_local_address_mac = ''
    
    with local.get_db() as db:
        _guild_value = local_rds.get_latest_local_profile(db, cli_commands.PROFILE_KEYS['GUILD_IS'])
        data_local_guild_is = True if _guild_value is not None and _guild_value == '1' else False
        
        _guild_unique_id = local_rds.get_latest_local_profile(db, cli_commands.PROFILE_KEYS['GUILD_UNIQUE_ID'])
        data_local_unique_id = _guild_unique_id if _guild_unique_id is not None else ''
        
        _guild_token = local_rds.get_latest_local_profile(db, cli_commands.PROFILE_KEYS['GUILD_TOKEN'])
        data_local_guild_token = _guild_token if _guild_token is not None else ''
        
        _outer_ip = local_rds.get_latest_local_profile(db, cli_commands.PROFILE_KEYS['GUILD_ADDRESS_OUTER_IP'])
        data_local_address_outer_ip = _outer_ip if _outer_ip is not None else ''
        
        _inner_ip = local_rds.get_latest_local_profile(db, cli_commands.PROFILE_KEYS['GUILD_ADDRESS_INNER_IP'])
        data_local_address_inner_ip = _inner_ip if _inner_ip is not None else ''
        
        _mac = local_rds.get_latest_local_profile(db, cli_commands.PROFILE_KEYS['GUILD_ADDRESS_MAC'])
        data_local_address_mac = _mac if _mac is not None else ''
        
    
        
    with conn.get_db() as db:
        discover = rds.get_service_discover_by_credentials(db, data_local_unique_id, data_local_guild_token)
        if data_local_guild_is:
            
            cli_commands.master_node_start()
            
            # 없으면 공용 데이터베이스에 등록. 이후 슬레이브가 마스터를 최초 및 갱신 시 조회하기 위해 사용됨.
            if discover == None:
                rds.register_service_discover(db, data_local_unique_id, data_local_guild_token, data_local_address_outer_ip, data_local_address_inner_ip, data_local_address_mac)
                
            
        
        
    

    
    
    
    
    
    try:
        
        ###=======================================
        ### 명령어 등록
        ###=======================================
        # 루트 추가/삭제/시작/중지/재시작/상태보기
        console.add_command("root-add", cli_commands.empty)                 # 루트 추가
        console.add_command("root-restart", cli_commands.empty)             # 루트 재시작
        console.add_command("root-remove", cli_commands.empty)              # 루트 삭제
        console.add_command("root-start", cli_commands.empty)               # 루트 시작
        console.add_command("root-stop", cli_commands.empty)                # 루트 중지
        console.add_command("root-status", cli_commands.empty)              # 루트 상태 보기
        
        
        # 루트에 관련된 정보 명령어
        console.add_command("root-get-branch-count", cli_commands.empty)                # 루트에 속한 브랜치 수 보기
        console.add_command("root-get-leaf-count", cli_commands.empty)                  # 루트에 속한 리프 수 보기
        console.add_command("root-get-leaf-count-with-mime", cli_commands.empty)        # 루트에 속한 리프 수 보기

        # 루트 정보를 업데이트
        console.add_command("root-config-update", cli_commands.empty)           # 루트 정보를 수정함. 이 과정 후 root를 재시작 해야함.
        
        # 탐색 시작/중지
        console.add_command("data-stop-branch-growing", cli_commands.empty)     # root를 켜서 queue 소비는 하는데 더 이상 확장 가능한 링크를 추가하지 않음
        console.add_command("data-start-branch-growing", cli_commands.empty)    # root를 껐던걸 다시 켜서 링크를 추가하길 시작함
        
        # api 서비스 시작/중지/상태보기/포트변경
        console.add_command("api-server-start", cli_commands.empty)             # api 서버 시작
        console.add_command("api-server-stop", cli_commands.empty)              # api 서버 중지
        console.add_command("api-server-status", cli_commands.empty)            # api 서버 상태 보기
        console.add_command("api-server-port-change", cli_commands.empty)       # api 서버 포트 변경
        
        console.add_command("dashboard-start", cli_commands.empty)    # dashboard start
        console.add_command("dashboard-stop", cli_commands.empty)     # dashboard stop
        console.add_command("dashboard-status", cli_commands.empty)   # dashboard status
        console.add_command("dashboard-port-change", cli_commands.empty) # dashboard server port change
        
        
        # rabbitmq 관련 명령어
        console.add_command("rq-sampling", cli_commands.empty)       # 큐 데이터 추출해서 보기
        console.add_command("rq-purge", cli_commands.empty)          # 큐 데이터 날리기
        console.add_command("rq-purge-all", cli_commands.empty)      # 모든 큐 데이터 날리기
        console.add_command("rq-delete-queue", cli_commands.empty)
        console.add_command("rq-delete-queue-all", cli_commands.empty)
        console.add_command("rq-delete-queue-bind", cli_commands.empty)
        console.add_command("rq-delete-queue-bind-all", cli_commands.empty)
        console.add_command("rq-delete-exchange", cli_commands.empty)
        console.add_command("rq-delete-exchange-all", cli_commands.empty)
        console.add_command("rq-show-queue-count", cli_commands.empty)
        console.add_command("rq-show-queue-count-all", cli_commands.empty)
        
        
        
        
        # 소스코드로 입력된 데이터를 조회하는 것
        console.add_command("source-get-roots", cli_commands.empty)         # 소스코드로 입력된 루트 정보를 보기
        console.add_command("source-get-ai-module", cli_commands.empty)     # 소스코드로 입력된 모듈 정보를 보기
        
        
        
        # 분산 처리 동작 클라이언트간 협업 (파티) 관련 명령어
        console.add_command("guild-stand-up", cli_commands.master_node_start)                   # 길드 설립 (마스터 노드가 되기)
        console.add_command("guild-info", cli_commands.empty)                                   # 모든 파티의 정보 보기 (마스터 노드의 자식 노드 그룹의 정보)
        console.add_command("guild-registration", cli_commands.guild_registration)              # 자신을 길드에 등록합니다
        console.add_command("guild-unique-change", cli_commands.guild_unique_change)            # 기기명 변경
        console.add_command("party-make", cli_commands.empty)                                   # 파티 만들기 (자식 노드 그룹 생성)
        console.add_command("party-join", cli_commands.empty)                                   # 파티에 참여하기 (자식 노드 그룹 참여)
        console.add_command("party-info", cli_commands.empty)                                   # 파티 정보 보기 (자식 노드 그룹의 정보)
        console.add_command("party-coop-change", cli_commands.empty)                            # 파티가 실행되는데 기준이 되는 방식
        console.add_command("party-assign-root", cli_commands.empty)                            # 파티에 속한 기기에 루트 추가하기
        console.add_command("party-marge", cli_commands.empty)                                  # 파티 2개를 1개로 합치기 (우측 기준 좌측으로 병합)


        
        
        
        # 버전 출력
        console.add_command("version", cli_commands.empty)
        
        # 입장 환영 메시지
        console.add_command("welcome", cli_commands.motd)
        
        # 개발용
        # console.add_command("@dev-migrate", cli_commands.dev__migrate) # 마이그레이션 테스트용
        console.add_command("@guild-stand-off", cli_commands.dev__master_node_stop) # 마이그레이션 테스트용

        # 업데이트 (대충 git page로 출력해서 비교하면 되는거 아님? ㅋㅋ)
        # 문제는 저장장치의 스키마 구조를 어떻게 바꿀것이냐 인데 라이브러리 의존도 여기는 성가셔짐.
        # console.add_command("version-update-check", cli_commands.empty)
        # console.add_command("version-update-letgo", cli_commands.empty)
        
        
        ###=======================================
        ### 메인스레드 콘솧 프로그램 실행 
        console.start(lambda: console.execute_command('welcome'))
        ###=======================================
        
    except KeyboardInterrupt:
        print("Exiting the program.")
    except Exception as e:
        print(f"An error occurred: {e}")


    ###=======================================
    ### 의도된 안정적인 종료 처리 (트리거는 메인스레드 종료에 의해 발생함)
    ###=======================================


    # 마스터 노드 있으면 종료
    if service_mesh_master.is_running():
        if service_mesh_master.stop():
            print("Master node stopped successfully.")
        else:
            print("Failed to stop master node.")

    # 모든 mq 연결에 종료를 시도함
    for mq_conn in all_mq_session:
        mq_conn.stop_consuming()
        
    # 모든 쓰레드를 종료처리함
    thread_manager.stop_all()
    
    #모든 쓰레드가 종료될때까지 대기함
    thread_manager.join_all()
    
    # rds db 를 닫음
    conn.close()
    local.close()
    
    # bye bye
    print("bye")
    return