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


rds_connection = Connection_Info()
rds_connection.db_type = DatabaseType.SQLITE3
rds_connection.database = "test.db"


# start client example
client_start(
    db_connection=rds_connection,
    roots=[
        Scrapper_Root('google', 'https://www.google.com', Scrapper_Root_Access_Rule(
            skip_uri_duplication=True, # URI 중복을 건너뛰는지 여부
            )),
    ]
)