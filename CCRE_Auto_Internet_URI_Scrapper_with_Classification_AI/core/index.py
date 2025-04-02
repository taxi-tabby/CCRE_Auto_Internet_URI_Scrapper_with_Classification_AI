import asyncio
import time

import pika
from sqlalchemy import text
from urllib.parse import urlparse


from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.rds import get_branch_id_if_exists, get_exists_branch, get_root_branch_count, table_init, get_roots_list, update_branches, update_leaves, update_roots
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.crawing import fetch_with_redirects
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.mime import get_mime_type_from_binary
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.parser.json import parse_json_string
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.parser.robots import check_robot_permission
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.parser.uri import normalize_uri_path
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.parser.xml import  extract_links_from_xml
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.string import shorten_string
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.stringify.json import stringify_to_json
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.connection_info import Connection_Info
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.pika_rabbitmq import PikaRabbitMQ
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.scrapper_root import Scrapper_Root
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.sqlalchemy import SQLAlchemyConnection
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.thread_manager import ThreadManager
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.db.models import *
from .import_path import add_module_path
from datetime import datetime


##-------------------------------------------------------------------------------
##-------------------------------------------------------------------------------
## constants
##-------------------------------------------------------------------------------
USER_AGENT_NAME = "CCRE_URI_CRAWLER/1.0/dev" # User-Agent 이름

CUSTOM_HEADER = {
    "User-Agent": USER_AGENT_NAME, 
    "User-Agent-Source": "https://github.com/taxi-tabby/CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI"
}

MAX_DIRECT_HTTP = 3 # 최대 허용 리다이렉트 수

##-------------------------------------------------------------------------------
##-------------------------------------------------------------------------------
##-------------------------------------------------------------------------------



def thlog(root_key: str, *args):
    """쓰레드 로그 출력용 함수."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] [{root_key}] {' '.join(args)}")


def _worker_start_ingot(root: Roots, db_session: SQLAlchemyConnection, mq_session: PikaRabbitMQ, ):
    """워커 연결용 함수.
    Args:
        root (Scrapper_Root): root 정보가 포함된 데이터
        db_session (SQLAlchemyConnection): rds 요청용 데이터베이스 세션
        mq_session (PikaRabbitMQ): 메세지 큐를 요청하거나 소비하기 위한 세션
    """
    
    thlog(root.root_key, f"worker start")
    
    config = {
        'exchange_name': f'{root.root_key}.exchange',
        'queue_name': f'{root.root_key}.queue',
        'route_key': f'{root.root_key}.direct_route'
    }


    mq_session.declare_exchange(config['exchange_name'], 'direct', durable=True, )
    mq_session.declare_queue(config['queue_name'], durable=True)
    mq_session.bind_queue(config['exchange_name'], config['queue_name'], config['route_key'])
    
    
    async def crawling_and_queuing(id: int | None, uri: str):
        try:


            ## robots.txt 체크
            if not check_robot_permission(uri, robot_name=USER_AGENT_NAME):
                return

            final_response = await fetch_with_redirects(uri, max_redirects=MAX_DIRECT_HTTP, headers=CUSTOM_HEADER)
            
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
                # thlog(root.root_key, f"Queue upload [{id}] - {idx}/{link_length}")
            
                
        except ValueError as ve:
            thlog(root.root_key, 'crawling value error - ', ve)
        except Exception as e:
            thlog(root.root_key, 'crawling except - ',e)


    # 루트에 브렌치 데이터가 없으면 크롤링 요청
    flag_branch_no_exists = False 
    with db_session.get_db() as db:
        cnt = get_root_branch_count(db, root.id)
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
        obj = parse_json_string(body)
        
        parent_id = obj['id']
        
        thlog(root.root_key, f"Queue received: parent_id: {parent_id}, uri:{shorten_string(obj['url'], 40)}, relative:{obj['is_relative']}")
        
        
        # 브랜치 등록 체크
        def dup_chk(root_id: int, uri: str) -> (int | None):
            with db_session.get_db() as db:
                return get_branch_id_if_exists(db, root_id, uri)


        # 브렌치가 존재하면 브랜치 생성
        def branch_up(id: int | None, uri: str) -> (int | None):
            with db_session.get_db() as db:
                branch = Branches()
                branch.id = None
                branch.parent_id = id
                branch.root_id = root.id
                branch.branch_uri = uri
                ids = update_branches(db, branches=[branch])
                if ids:
                    return ids[0]
                return None


        # 브렌치가 존재하지 않으면 새로 생성
        async def leaf_up(id: int | None, uri: str) -> (int | None):
            
            final_response = await fetch_with_redirects(uri, max_redirects=MAX_DIRECT_HTTP, headers=CUSTOM_HEADER)
            content_type = final_response['content_type']
            http_body = final_response['body']
            mime = get_mime_type_from_binary(http_body.encode() if isinstance(http_body, str) else http_body)
            
            if isinstance(http_body, bytes):
                mime = get_mime_type_from_binary(http_body)
            else:
                mime = get_mime_type_from_binary(http_body.encode())

            if mime == "application/octet-stream" and content_type != mime:
                mime = content_type
                    
            with db_session.get_db() as db:
                leaf = Leaves()
                leaf.id = None
                leaf.root_id = root.id
                leaf.branch_id = id
                leaf.val_classified = 'none-test'
                leaf.val_mime_type = mime
                
                ids = update_leaves(db, leaves=[leaf])
                if ids:
                    return ids[0]
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
                    
                if d2 == None:
                    id = branch_up(parent_id, assembled_uri_no_path)
                    # print(f"branch id: {parent_id} / {id}")
                    if not id == None:
                        asyncio.run(crawling_and_queuing(id, assembled_uri_no_path))
                        asyncio.run(leaf_up(id, assembled_uri_no_path))
                
            else:
                # 절대경로
                assembled_uri = obj['url']
                
                if not dup_chk(root.id, assembled_uri):
                    id = branch_up(parent_id, assembled_uri)
                    # print(f"branch id: {parent_id} / {id}")
                    if not id == None:
                        asyncio.run(crawling_and_queuing(id, assembled_uri))
                        asyncio.run(leaf_up(id, assembled_uri))
                




        except Exception as e:
            pass
        
    thlog(root.root_key, f'start consuming')
    
    # 메세지 큐 소비
    mq_session.set_qos(1)
    mq_session.b_consume(config['queue_name'], callback, delay_sec=0.1)
    
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
    
    print("hello")
    
    conn = SQLAlchemyConnection()
    conn.connection = db_rds_connection
    print("db connection initialized")
    
    

    
    all_roots: list[Roots] = []
    
    with conn.get_db() as db:
        # rds db table init
        table_init(conn._engine, db, db_rds_connection.db_type) # 테이블 생성
        update_roots(db, roots) # root 정보 업데이트

        # 모든 root를 획득.
        page_n: int = 1
        while True:
            new_roots = get_roots_list(db, page_n)
            if not new_roots:
                break
            all_roots.extend(new_roots)
            page_n += 1
        
    
    
    thread_manager = ThreadManager()
    thread_manager.add_watcher(check_interval=2)
    
    all_mq_session: list[PikaRabbitMQ] = []
    
    for i, root in enumerate(all_roots):
        # make mq connection
        mq_conn = PikaRabbitMQ()
        mq_conn.connect(db_mq_connection.host, db_mq_connection.port, db_mq_connection.user, db_mq_connection.password, db_mq_connection.vhost)
        mq_conn.declare_channel()
        
        # append mq session for closing
        all_mq_session.append(mq_conn)
        
        # add worker
        thread_manager.add_worker(target=_worker_start_ingot, args=(root, conn, mq_conn, ), thread_id=i)
        
    # start all thread
    thread_manager.start_all()
    
    try:
        while True:
            time.sleep(5)  
    except KeyboardInterrupt:
        print("Exiting the program.")
        for mq_conn in all_mq_session:
            mq_conn.stop_consuming()
    except Exception as e:
        print(f"An error occurred: {e}")
        for mq_conn in all_mq_session:
            mq_conn.stop_consuming()
        
    thread_manager.stop_all()
    thread_manager.join_all()
    
    # rds db close
    conn.close()
    
    # bye bye
    print("bye")
    return