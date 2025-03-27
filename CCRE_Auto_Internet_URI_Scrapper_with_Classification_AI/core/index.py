import time

from sqlalchemy import text
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.rds import get_root_branch_count, table_init, get_roots_list, update_roots
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.crawing import fetch_with_redirects
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.parser.json import parse_json_string
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.parser.xml import  extract_links_from_xml
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.stringify.json import stringify_to_json
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.connection_info import Connection_Info
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.pika_rabbitmq import PikaRabbitMQ
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.scrapper_root import Scrapper_Root
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.sqlalchemy import SQLAlchemyConnection
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.thread_manager import ThreadManager
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.db.models import *
from .import_path import add_module_path



def _worker_start_ingot(root: Roots, db_session: SQLAlchemyConnection, mq_session: PikaRabbitMQ, ):
    """워커 연결용 함수.
    Args:
        root (Scrapper_Root): root 정보가 포함된 데이터
        db_session (SQLAlchemyConnection): rds 요청용 데이터베이스 세션
        mq_session (PikaRabbitMQ): 메세지 큐를 요청하거나 소비하기 위한 세션
    """
    
    print(f"worker start: {root.root_key}")
    
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
    
    
    def crawing_and_queuing(uri: str):
        try:
            custom_headers = {
                "User-Agent": "CCRE_URI_CRAWING", 
                "User-Agent-Source": "https://github.com/taxi-tabby/CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI"
                }
            final_response = fetch_with_redirects(uri, headers=custom_headers, max_redirects=5)
            links = extract_links_from_xml(final_response['body'])
            
            for link in links:
                mq_session.b_publish(config['exchange_name'], config['route_key'], stringify_to_json(link))
                
        except Exception as e:
            print(f"Error: {e}")

    flag_branch_no_exists = False 
    with db_session.get_db() as db:
        cnt = get_root_branch_count(db, root.id)
        if cnt == 0:
            flag_branch_no_exists = True
    
    
    # 최초에 브렌치 데이터 없으면 요청해서 메세지 큐를 생성. 
    if flag_branch_no_exists:
        crawing_and_queuing(root.root_uri)
        
    # 메세지 큐 소비 처리
    def callback(ch, method, properties, body):
        obj = parse_json_string(body)

        assembled_uri = obj['url']
        if obj['is_relative']:
            assembled_uri = root.root_uri + obj['url']
            
        print(f" [{root.root_key}] Queue received {obj} and crawling {assembled_uri}")
        crawing_and_queuing(assembled_uri)
    
    # 메세지 큐 소비
    mq_session.b_consume(config['queue_name'], callback, delay_sec=0.1)



    
    print(f"worker process complete: {root.root_key}")
    















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