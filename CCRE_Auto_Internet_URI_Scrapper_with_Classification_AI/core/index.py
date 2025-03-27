import time

from sqlalchemy import text
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.rds import table_init, get_roots_list, update_roots
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.crawing import fetch_with_redirects
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.connection_info import Connection_Info
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.pika_rabbitmq import PikaRabbitMQ
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.scrapper_root import Scrapper_Root
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.sqlalchemy import SQLAlchemyConnection
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.thread_manager import ThreadManager
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.db.models import *
from .import_path import add_module_path



def _worker_start_ingot(root: (Scrapper_Root|Roots), db_session: SQLAlchemyConnection, mq_session: PikaRabbitMQ):
    """워커 연결용 함수.

    Args:
        root (Scrapper_Root): root 정보가 포함된 데이터
        db_session (SQLAlchemyConnection): rds 요청용 데이터베이스 세션
        mq_session (PikaRabbitMQ): 메세지 큐를 요청하거나 소비하기 위한 세션
    """


    print(f"worker start: {root.root_key}")
    
    # 테스트 실행
    
    try:
        custom_headers = {
            "User-Agent": "CCRE_URI_CRAW_CLIENT/1.0", 
            "User-Agent-Source": "https://github.com/taxi-tabby/CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI"
            }
        final_response = fetch_with_redirects(root.root_uri, headers=custom_headers)
        print(final_response['headers'])
    except Exception as e:
        print(f"Error: {e}")
        
    
    with db_session.get_db() as db:
        # 테스트 발행. 잘 대는고만. 이제 동적 생성만 하면 대겠네
        # Check if the table exists
        # mq_session.b_publish("test.exchange", "test.routing.#", "helloworld1")
        # db.execute(text('SELECT 1'))
        pass
    
    print(f"worker process complete: {root.root_key}")
    
    
    pass




def initialize(
    db_rds_connection: Connection_Info, # db storage connection info
    db_mq_connection: Connection_Info, # db storage connection info
    roots: list[Scrapper_Root] # root list
    ):
    
    add_module_path("../")
    
    print("hello")
    
    conn = SQLAlchemyConnection()
    conn.connection = db_rds_connection
    print("db connection initialized")
    
    
    mq_conn = PikaRabbitMQ()
    mq_conn.connect(db_mq_connection.host, db_mq_connection.port, db_mq_connection.user, db_mq_connection.password, db_mq_connection.vhost)
    mq_conn.declare_channel()
    print("mq connection initialized")
    
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
        
    
    print("all roots: ", all_roots)
    
    thread_manager = ThreadManager()
    thread_manager.add_watcher(check_interval=2)
    
    for i, root in enumerate(roots):
        thread_manager.add_worker(target=_worker_start_ingot, args=(root, conn, mq_conn,), thread_id=i)
        
    thread_manager.start_all()
    
    try:
        while True:
            time.sleep(1)  
    except KeyboardInterrupt:
        print("Exiting the program.")
        
    thread_manager.stop_all()
    thread_manager.join_all()
    
    # rds db close
    conn.close()
    
    # bye bye
    print("bye")
    return