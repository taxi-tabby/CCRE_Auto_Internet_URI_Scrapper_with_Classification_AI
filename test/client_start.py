
import sys
import os






# 테스트용 루트 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Source start line

from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.module import client_start
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.abstract.rds.predef import DatabaseType
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.connection_info import Connection_Info
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.scrapper_root import Scrapper_Root
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.scrapper_root_access_rule import Scrapper_Root_Access_Rule
from datetime import timedelta

# create rds db connection
rds_connection = Connection_Info()
rds_connection.db_type = DatabaseType.SQLITE3
rds_connection.database = "test.db"


# queue connection
rabbit_mq = Connection_Info()
rabbit_mq.db_type = DatabaseType.RABBITMQ
rabbit_mq.host = "localhost"
rabbit_mq.port = 5672
rabbit_mq.user = "test_user"
rabbit_mq.password = "1234"
rabbit_mq.vhost = "/"




# Options configuration
option = Scrapper_Root_Access_Rule(

    # Whether to skip duplicate URIs (False means it could loop endlessly on the same page)
    # [-------- NOT Applied --------]
    skip_duplication_uri=True, 

    # Whether to refresh duplicate URIs (Refreshing means re-evaluating and scoring the URI)
    # [-------- NOT Applied --------]
    refresh_duplicate_uri=True, 

    # Number of duplicate URIs before refreshing (Refresh happens if a URI is repeated more than this number)
    # [-------- NOT Applied --------]
    refresh_duplicate_uri_count=10,
    
    # robots.txt cache expiration time (set to 5 minutes)
    # [-------- Applied --------]
    robots_txt_expiration_time=timedelta(minutes=5),
    
    # Delay (in seconds) between consuming URIs 
    # [-------- Applied --------]
    consume_delay_seconds=1,  
    
    # Whether to save all accessible assets (set to False means assets won't be saved)
    # [-------- NOT Applied --------]
    save_all_accessible_assets=False,  
    
    # This is ignored if save_all_accessible_assets is False
    # MIME types of assets to save (only applies if saving assets is enabled)
    # [-------- NOT Applied --------]
    save_all_accessible_assets_mime_types=['text/html', 'application/pdf', 'image/jpeg', 'image/png', 'application/json'],
    
    # Whether to scan accessible assets for malware
    # This is ignored if save_all_accessible_assets is False
    # [-------- NOT Applied --------]
    scan_all_accessible_assets_for_malware=True,
    
    # This is ignored if scan_all_accessible_assets_for_malware is False
    # MIME types of assets to scan for malware (only applies if malware scanning is enabled)
    # [-------- NOT Applied --------]
    scan_all_accessible_assets_mime_types=['text/html', 'application/pdf', 'image/jpeg', 'image/png', 'application/json']
)



# start client example
client_start(
    db_rds_connection=rds_connection,
    db_mq_connection=rabbit_mq,
    roots=[
        Scrapper_Root('test_example1_kr', access_rule=option, root_uri='https://naver.com'),
        Scrapper_Root('test_example2_jp', access_rule=option, root_uri='https://www.yahoo.co.jp'),
        Scrapper_Root('test_example3_zh', access_rule=option, root_uri='https://baidu.com'),
    ]
)