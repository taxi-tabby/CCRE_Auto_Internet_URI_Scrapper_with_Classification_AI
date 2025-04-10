
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
# rds_connection = Connection_Info()
# rds_connection.db_type = DatabaseType.SQLITE3
# rds_connection.database = "test.db"

rds_connection = Connection_Info()
rds_connection.db_type = DatabaseType.POSTGRESQL
rds_connection.database = "test_1"
rds_connection.host = "localhost"
rds_connection.port = 5432
rds_connection.user = "postgres"
rds_connection.password = "15515995"



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
    
    # robots.txt cache expiration time (set to 10 minutes)
    # [-------- Applied --------]
    robots_txt_expiration_time=timedelta(minutes=10),
    
    # Delay (in seconds) between uploading to the queue
    # [-------- Applied --------]
    queue_upload_delay_seconds=1,
    
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
        # group0
        Scrapper_Root('test_example1_kr', access_rule=option, root_uri='https://naver.com'),
        Scrapper_Root('test_example2_jp', access_rule=option, root_uri='https://www.yahoo.co.jp'),
        Scrapper_Root('test_example3_zh', access_rule=option, root_uri='https://baidu.com'),
        Scrapper_Root('test_example4_indi', access_rule=option, root_uri='https://www.indiatimes.com'),
        Scrapper_Root('test_example5_ru', access_rule=option, root_uri='https://dzen.ru'),
        Scrapper_Root('test_example6_vie', access_rule=option, root_uri='https://coccoc.com'),
        Scrapper_Root('test_example7_en', access_rule=option, root_uri='https://www.yahoo.com'),
        
        # # group1
        Scrapper_Root('test_example8_us', access_rule=option, root_uri='https://www.google.com'),
        Scrapper_Root('test_example9_de', access_rule=option, root_uri='https://www.google.de'),
        Scrapper_Root('test_example10_fr', access_rule=option, root_uri='https://www.lefigaro.fr'),
        Scrapper_Root('test_example11_it', access_rule=option, root_uri='https://www.repubblica.it'),
        Scrapper_Root('test_example12_es', access_rule=option, root_uri='https://www.elmundo.es'),
        Scrapper_Root('test_example13_br', access_rule=option, root_uri='https://www.uol.com.br'),
        Scrapper_Root('test_example14_sa', access_rule=option, root_uri='https://www.sabq.org'),
        Scrapper_Root('test_example15_ae', access_rule=option, root_uri='https://www.thenationalnews.com'),
        Scrapper_Root('test_example16_ca', access_rule=option, root_uri='https://www.theglobeandmail.com'),
        Scrapper_Root('test_example17_au', access_rule=option, root_uri='https://www.smh.com.au'),
        Scrapper_Root('test_example18_kr2', access_rule=option, root_uri='https://daum.net'),
        Scrapper_Root('test_example19_tr', access_rule=option, root_uri='https://www.hurriyet.com.tr'),
        Scrapper_Root('test_example20_pl', access_rule=option, root_uri='https://www.onet.pl'),
        Scrapper_Root('test_example21_id', access_rule=option, root_uri='https://detik.com'),
        Scrapper_Root('test_example22_th', access_rule=option, root_uri='https://www.sanook.com'),
        Scrapper_Root('test_example23_ph', access_rule=option, root_uri='https://www.abs-cbn.com'),
        Scrapper_Root('test_example24_my', access_rule=option, root_uri='https://www.thestar.com.my'),
        Scrapper_Root('test_example25_eg', access_rule=option, root_uri='https://www.youm7.com'),
        Scrapper_Root('test_example26_ng', access_rule=option, root_uri='https://www.pulse.ng'),
        Scrapper_Root('test_example27_za', access_rule=option, root_uri='https://www.news24.com'),
        Scrapper_Root('test_example28_kr3', access_rule=option, root_uri='https://chosun.com'),
        Scrapper_Root('test_example29_ar', access_rule=option, root_uri='https://www.clarin.com'),
        Scrapper_Root('test_example30_kr4', access_rule=option, root_uri='https://hankyung.com'),
        Scrapper_Root('test_example31_se', access_rule=option, root_uri='https://www.aftonbladet.se'),
        Scrapper_Root('test_example32_no', access_rule=option, root_uri='https://www.dagbladet.no'),
        Scrapper_Root('test_example33_dk', access_rule=option, root_uri='https://www.bt.dk'),
        Scrapper_Root('test_example34_fi', access_rule=option, root_uri='https://www.hs.fi'),
        Scrapper_Root('test_example35_cn', access_rule=option, root_uri='https://so.com'),
        Scrapper_Root('test_example36_kr5', access_rule=option, root_uri='https://seoul.co.kr'),
        Scrapper_Root('test_example37_us2', access_rule=option, root_uri='https://www.bing.com'),
        Scrapper_Root('test_example38_fr2', access_rule=option, root_uri='https://www.lemonde.fr'),
        Scrapper_Root('test_example39_kr6', access_rule=option, root_uri='https://ytn.co.kr'),
        Scrapper_Root('test_example40_uk', access_rule=option, root_uri='https://www.bbc.co.uk'),
        
        # # group2
        Scrapper_Root('test_example41_kr7', access_rule=option, root_uri='https://news.daum.net'),
        Scrapper_Root('test_example42_in', access_rule=option, root_uri='https://timesofindia.indiatimes.com'),
        Scrapper_Root('test_example43_za2', access_rule=option, root_uri='https://www.timeslive.co.za'),
        Scrapper_Root('test_example44_eg2', access_rule=option, root_uri='https://www.almasryalyoum.com'),
        Scrapper_Root('test_example45_sa2', access_rule=option, root_uri='https://www.okaz.com.sa'),
        Scrapper_Root('test_example46_br2', access_rule=option, root_uri='https://www.globo.com'),
        Scrapper_Root('test_example47_ca2', access_rule=option, root_uri='https://www.cbc.ca'),
        Scrapper_Root('test_example48_au2', access_rule=option, root_uri='https://www.news.com.au'),
        Scrapper_Root('test_example49_ng2', access_rule=option, root_uri='https://www.vanguardngr.com'),
        Scrapper_Root('test_example50_tw', access_rule=option, root_uri='https://www.ettoday.net'),
        Scrapper_Root('test_example51_hk', access_rule=option, root_uri='https://www.hk01.com'),
        Scrapper_Root('test_example52_my2', access_rule=option, root_uri='https://www.malaymail.com'),
        Scrapper_Root('test_example53_ke', access_rule=option, root_uri='https://www.standardmedia.co.ke'),
        Scrapper_Root('test_example54_ng3', access_rule=option, root_uri='https://www.thecable.ng'),
        Scrapper_Root('test_example55_in2', access_rule=option, root_uri='https://www.ndtv.com'),
        Scrapper_Root('test_example56_ar2', access_rule=option, root_uri='https://www.lanacion.com.ar'),
        Scrapper_Root('test_example57_kr8', access_rule=option, root_uri='https://tvchosun.com'),
        Scrapper_Root('test_example58_gr', access_rule=option, root_uri='https://www.protothema.gr'),
        Scrapper_Root('test_example59_cz', access_rule=option, root_uri='https://www.idnes.cz'),
        Scrapper_Root('test_example60_ro', access_rule=option, root_uri='https://www.digi24.ro'),
        Scrapper_Root('test_example61_bh', access_rule=option, root_uri='https://www.albiladpress.com'),
        Scrapper_Root('test_example62_qa', access_rule=option, root_uri='https://www.aljazeera.net'),
        Scrapper_Root('test_example63_ae2', access_rule=option, root_uri='https://www.khaleejtimes.com'),
        Scrapper_Root('test_example64_jm', access_rule=option, root_uri='https://www.jamaicaobserver.com'),
        Scrapper_Root('test_example65_hu', access_rule=option, root_uri='https://www.index.hu'),
    ]
)
