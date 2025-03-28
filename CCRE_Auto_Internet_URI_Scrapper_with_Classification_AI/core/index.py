import time

import pika
from sqlalchemy import text
from urllib.parse import urlparse


from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.rds import get_branch_id_if_exists, get_exists_branch, get_root_branch_count, table_init, get_roots_list, update_branches, update_roots
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.crawing import fetch_with_redirects
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.parser.json import parse_json_string
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


def thlog(root_key, *args):
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
        'route_key': f'{root.root_key}.route.#'
    }
    
    



    # if not mq_conn.exists_exchange(config['exchange_name']):
    mq_session.declare_exchange(config['exchange_name'], 'direct', durable=True, )
        
    # if not mq_conn.exists_queue(config['queue_name']):
    mq_session.declare_queue(config['queue_name'], durable=True)
        
    # if not mq_conn.exists_bind(config['exchange_name'], config['queue_name'], config['route_key']):
    mq_session.bind_queue(config['exchange_name'], config['queue_name'], config['route_key'])
    
    
    def crawling_and_queuing(id: int | None, uri: str):
        try:
            custom_headers = {
                "User-Agent": "CCRE_URI_CRAWING", 
                "User-Agent-Source": "https://github.com/taxi-tabby/CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI"
                }
            final_response = fetch_with_redirects(uri, headers=custom_headers, max_redirects=3)
            links = extract_links_from_xml(final_response['body'])
            for link in links:
                link['id'] = id
                mq_session.b_publish(config['exchange_name'], config['route_key'], stringify_to_json(link))
                
        except Exception as e:
            thlog(root.root_key, 'crawling except - ',e)
            pass



    # 루트에 브렌치 데이터가 없으면 크롤링 요청
    flag_branch_no_exists = False 
    with db_session.get_db() as db:
        cnt = get_root_branch_count(db, root.id)
        if cnt == 0:
            flag_branch_no_exists = True
    
    

    # 최초에 브렌치 데이터 없으면 요청해서 메세지 큐를 생성. 
    if flag_branch_no_exists:
        try:
            crawling_and_queuing(None, root.root_uri)
            thlog(root.root_key, f"first branch creation done")
        except Exception as e:
            thlog(root.root_key, f"root init crawling error", e)
        
    
    
        
        
    # 메세지 큐 소비 처리
    def callback(ch: pika.channel.Channel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes):
        obj = parse_json_string(body)
        thlog(root.root_key, f"Queue received: uri:{shorten_string(obj['url'], 40)}, relative:{obj['is_relative']}")
        
        def dup_chk(root_id: int, uri: str) -> (int | None):
            with db_session.get_db() as db:
                return get_branch_id_if_exists(db, root_id, uri)



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

        try:
            if obj['is_relative']:
                # 상대경로
                parsed_url = urlparse(root.root_uri)
                assembled_uri_with_path = normalize_uri_path(f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}{obj['url']}")
                assembled_uri_no_path = normalize_uri_path(f"{parsed_url.scheme}://{parsed_url.netloc}{obj['url']}")
                
                d1 = dup_chk(root.id, assembled_uri_with_path)
                d1_id = obj['id']
                d2 = dup_chk(root.id, assembled_uri_no_path)
                d2_id = obj['id']
                
                if not d1 == None:
                    d1_id = d1 
                    
                if not d2 == None:
                    d2_id = d2 
                
                if d1 == None:
                    id = branch_up(d1_id, assembled_uri_with_path)
                    if not id == None:
                        crawling_and_queuing(id, assembled_uri_with_path)
                    
                if d2 == None:
                    id = branch_up(d2_id, assembled_uri_no_path)
                    if not id == None:
                        crawling_and_queuing(id, assembled_uri_no_path)
                
            else:
                # 절대경로
                assembled_uri = normalize_uri_path(obj['url'])
                dd = dup_chk(root.id, assembled_uri)
                dd_id = obj['id']
                
                if not dd == None:
                    dd_id = dd
                
                if not dup_chk(root.id, assembled_uri):
                    id = branch_up(dd_id, assembled_uri)
                    if not id == None:
                        crawling_and_queuing(id, assembled_uri)
                




        except Exception as e:
            pass
        
    thlog(root.root_key, f'start consuming')
    
    # 메세지 큐 소비
    mq_session.b_consume(config['queue_name'], callback, delay_sec=3)
    
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
            time.sleep(1)  
    except KeyboardInterrupt:
        print("Exiting the program.")
        for mq_conn in all_mq_session:
            mq_conn.stop_consuming()
        
    thread_manager.stop_all()
    thread_manager.join_all()
    
    # rds db close
    conn.close()
    
    # bye bye
    print("bye")
    return