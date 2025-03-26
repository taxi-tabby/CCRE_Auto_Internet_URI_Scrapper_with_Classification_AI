import time
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.connection_info import Connection_Info
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.scrapper_root import Scrapper_Root
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.sqlalchemy import SQLAlchemyConnection
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.thread_manager import ThreadManager
from .import_path import add_module_path

def _addPath():
    add_module_path("../")



def _test_worker(db_session: SQLAlchemyConnection):
    # print(n)
    n += 1
    print("test worker", n)
    print("process complete")
    pass




def initialize(
    db_connection: Connection_Info, # db storage connection info
    roots: list[Scrapper_Root] # root list
    ):
    _addPath()
    
    
    conn = SQLAlchemyConnection()
    conn.connection = db_connection
    
    
    
    
    thread_manager = ThreadManager()
    thread_manager.add_watcher(check_interval=2)
    
    for i, root in enumerate(roots):
        thread_manager.add_worker(target=_test_worker, args=(root,), thread_id=i)
        
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