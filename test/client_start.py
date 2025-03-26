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


# create rds db connection
rds_connection = Connection_Info()
rds_connection.db_type = DatabaseType.SQLITE3
rds_connection.database = "test.db"


rabbit_mq = Connection_Info()
rabbit_mq.db_type = DatabaseType.RABBITMQ
rabbit_mq.host = "localhost"
rabbit_mq.port = 5672
rabbit_mq.user = "test_user"
rabbit_mq.password = "1234"
rabbit_mq.vhost = "/"




# start client example
client_start(
    db_rds_connection=rds_connection,
    db_mq_connection=rabbit_mq,
    roots=[
        Scrapper_Root('google', 'https://www.google.com', Scrapper_Root_Access_Rule(
            
            # URI 중복을 건너뛰는지 여부 (False 인 경우 특정 페이지를 무한하게 순환할 가능성이 있음.)
            skip_duplication_uri=False, 
            
            # URI 중복을 갱신하는지 여부 (갱신은 해당 URI를 다시 분별하고 점수를 매기는 것을 의미합니다)
            refresh_duplicate_uri=False, 
            # URI 중복이 어느정도 누적되면 갱신할지 
            refresh_duplicate_uri_count=0 
            
            )),
    ]
)