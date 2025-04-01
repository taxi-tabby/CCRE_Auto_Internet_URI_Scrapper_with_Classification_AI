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


# queue connection
rabbit_mq = Connection_Info()
rabbit_mq.db_type = DatabaseType.RABBITMQ
rabbit_mq.host = "localhost"
rabbit_mq.port = 5672
rabbit_mq.user = "test_user"
rabbit_mq.password = "1234"
rabbit_mq.vhost = "/"




# option
option = Scrapper_Root_Access_Rule(

    # Whether to skip duplicate URIs (If False, it may endlessly loop on a specific page.)
    skip_duplication_uri=True, 

    # Whether to refresh duplicate URIs (Refreshing means re-evaluating and scoring the URI.)
    refresh_duplicate_uri=True, 

    # Threshold count of duplicate URIs before refreshing
    refresh_duplicate_uri_count=10 

)


# start client example
client_start(
    db_rds_connection=rds_connection,
    db_mq_connection=rabbit_mq,
    roots=[
        Scrapper_Root('test_example0', access_rule=option, root_uri='https://www.google.com/search?q=illegal+drug+dealer+onion&sca_esv=e1bc306dcb0911c4&sxsrf=AHTn8zrGlBOL_M0ZanIb6qofVWRZu9qO7Q%3A1743102271430&ei=P6HlZ8SGGsvf2roPnZ-XgAI&ved=0ahUKEwiEosj9-aqMAxXLr1YBHZ3PBSAQ4dUDCBA&uact=5&oq=illegal+drug+dealer+onion&gs_lp=Egxnd3Mtd2l6LXNlcnAiGWlsbGVnYWwgZHJ1ZyBkZWFsZXIgb25pb24yBxAhGKABGAoyBxAhGKABGAoyBBAhGBUyBBAhGBUyBBAhGApI4hFQ_QRY9xBwAXgAkAEAmAGZAaABoQWqAQMwLjW4AQPIAQD4AQGYAgWgAqsEwgIJEAAYsAMYBxgewgIJEAAYsAMYCBgewgIFECEYoAGYAwCIBgGQBgaSBwMxLjSgB9gSsgcDMC40uAepBA&sclient=gws-wiz-serp'),
        Scrapper_Root('test_example1', access_rule=option, root_uri='https://example.com'),
        Scrapper_Root('test_example2', access_rule=option, root_uri='https://smallbrain-labo.work/'),
    ]
)