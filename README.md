# CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI

URI 싹싹 긁어 모으는 기능을 가지고 있습니다.

아직 개발하고 있고 개량을 거치면 더 좋아지겠네요

덕덕고, 구글, 야후, 네이버 같은 검색엔진이 순회하면서 사이트 정보를 얻듯 다양한 위치에서 URI를 얻고 분별, 평가하여 RDS DB에 실시간으로 저장합니다.

풀어선 뭐 검색엔진 봇이죠 봇.

코드상에서 설정하여 이미지는 이미지별로, HTML 문서나 폰트파일 등에 대해 개발자가 지정하여 모델을 적용하고 자동으로 평가하게 할 수 있도록 하는것이 목표입니다

RABBITMQ + RDS DB로 구성된 만큼 관리하는데 어려움이 있으며 추후에는 GUI로 만들어지면 좋겠네요.

root라는 단위는 시작점을 기리키는 uri이고 해당 기준으로 설정을 가지고 있으며 root의 갯수만큼 쓰레드를 생성하고 실행됩니다.

외부 서버를 계속 긁어서 데이터를 입력 및 업데이트 하는 만큼 피해가 덜하도록 하는 작업이 수반되야 하네요

이걸 안하면 악성코드랑 차이가 없어지고 하니 ㅋㅋ 




영어로 쓰는건 나중에 해야지




### dependency:
- sqlalchemy (data storage)
- pika (rabbitmq)
- aiohttp (async http request)
- python-magic, python-magic-bin (binary mime check)
- pytz (time library)
- beautifulsoup4 (html parse)
- prompt_toolkit (cli console)
- yara, maltrail (ANTI VIRUS 1) (아직 안썼음)
- pyclamd (ANTI VIRUS 2) (아직 안썼음)
- psycopg2 (postgresql)
- psutil (etc) (이후 제거 가능성 있음)
- alembic (rds migrate)

### tools
- rabbitMQ
- RDS DB

### features
- crawling

### additional features
- Distributed bypass ICMP check (openvpn)
- Scan after Javascript rendering (selenium)


### ref
https://huggingface.co/





### devlog


#### 2025.04.21

1. 프로젝트 진행하면서 Obsidian 을 아에 프로젝트에 박아버리면 협업에서 도움될련지 확인.
2. 이론 문서랑 왕도인 패턴 같은거 확인하는 중.

```console
> guild-join --ip 127.0.0.1 --port 12345 --token 000
You are not allowed to be a slave. you are the master node. sir
```


#### 2025.04.14 (2)

```console
hello
Connection 12c3d240-61b6-4aa7-a653-73afd200a3f9 initialized with DatabaseType.SQLITE3 database
Connection 461c80fe-e8a7-4756-95e1-22908a7759fd initialized with DatabaseType.SQLITE3 database

        ╔════════════════════════════════════════════════════════╗
        ║                                                        ║
        ║   CCRE Auto Internet URI Scrapper with Classification  ║
        ║                                                        ║
        ╚════════════════════════════════════════════════════════╝


System: Windows 10
Time: 2025-04-14 05:40:10

[This client stat]
GUILD_UNIQUE_ID: MasterNode
GUILD_IS: 1
GUILD_ADDRESS_OUTER_IP: ###.237.###.144
GUILD_ADDRESS_INNER_IP: 192.168.0.10
GUILD_ADDRESS_MAC: ##:1a:##:da:##:13
GUILD_LAST_RG_AT: 2025-04-13 21:03:23
GUILD_TOKEN: 4417b056e8e07a0ce4dfe2a794aa3dba03b5c67b7257822103ff526fe40701416a8b8199b68cbd340f5d709ecc7a982c64a1ea96808e66ef0834b8aa72622a10
> guild-stand-up
Master node initialized: 0.0.0.0 / open is True / address is 12345
Master node started successfully.
> exit
클라이언트 처리 중 오류: [WinError 10038] 소켓 이외의 개체에 작업을 시도했습니다
Master node stopped successfully.
watcher thread signaled to stop
Closing connection 12c3d240-61b6-4aa7-a653-73afd200a3f9
Closing connection 461c80fe-e8a7-4756-95e1-22908a7759fd
bye
```

#### 2025.04.15 (1)

alembic 결국 쓰기로 했음. 컬럼 바뀌는데 하나하나 다 맞춰주기 힘들어서 앞으론 이걸로 편할듯


#### 2025.04.14 (1)

계속 욕심을 부리는데. 이거 점점 사이즈가 커진다.
분산 처리 관리를 위한 마스터-슬레이브 서비스 매시를 구현해서
쓸 수 있도록 하고 싶은데


거기에 node 기반 대시보드 구축하고. 필요에 따라선 룰 기반 규칙 또는 좀 더 경량회된 인증체계 구축이랑 (존맛탱 토큰은 구려서 안씀 개구림)
그렇게 인증체계가 구축되면 대시보드용 API 를 붙이고
cli 또는 커맨드, 대시보드에 접근해서 명령어를 입력할 수 있도록 해야함.
당연 cli 명령어를 동작하도록 연결필수

그걸 전부 다 해야 최소한의 알파버전이 나오는걸로 보고있다.

다 혼자하는거라 더 걸리겠지. 분명 욕심부릴꺼야 더 멋지게 한다고. 시간 제한도 없는데.


#### 2025.04.11 (1)

> RDS를 외부로 빼서 분산 처리
![4-3.gif](./readme/6.png)

#### 2025.04.10 (2)

그리고 지금 중복체크를 uri 그대로 하는데. 당연하게도 이러면 빅데이터가 쌓였을 때 감당이 안댐.
아무리 btree가 빠르다고 해도 색인할 키가 필요하니 uri에 대해 유효한 방식으로 키 생성해서 익덱싱 되도록 해야 함.
풀텍스트 인덱스 피하는건 가능하겠네 uri이니 / segment 같은 보편적인 기준이 있다.

```console
[2025-04-09 19:02:15] [test_example3_zh] leaf_up error: The markup you provided was rejected by the parser. Trying a different parser or a different encoding may help.

Original exception(s) from parser:
 AssertionError: expected name token at '<![\\7\x0ckQgz\x10?e[\x7fLS\x04s>'
 ```


#### 2025.04.10 (1)

이제 명령어 입력되면 받아서 중간자에서 동작하는 프로세스 하나 더 만들어서 돌리면 좀 사용성 오를 듯.

![4-3.gif](./readme/5.png)

#### 2025.04.09 (1)

사용자 접근성을 위한 웹 로컬 대시보드 어찌고가 필요해 보임. 그리고
console 쪽 개편도 필요하고. 
약간 불편한 부분을 바꿀 필요가 있음. 
나 조차 이러면 불편하겠다 하는 부분이 있는데 그냥 넘어가기엔 그렇지.

#### 2025.04.08 (1)

##### 대시보드 로컬 웹 프레임워크 선정의 시간.
1. FastAPI
- 그닥..
2. Plotly Dash
- 그닥..
1. Streamlit    (https://docs.streamlit.io/develop/api-reference)
- 제한적임. 그냥 오픈소스 노션 제작 툴.
1. Flask        (틀)
- 안써요 안써.
1. Django       (ㅌ)
- 구려요 구려.
1. Reflex       (https://reflex.dev/templates/)
- 좋아보이는데? 좋아보여도 그냥 node를 쓰고 말지란 느낌인데.
node모르면 배우기 귀찮은 사람이 쓸 것 같다.

그래도 아무리 그래도..
진짜 1황은 node가 다 먹었다.
굳이 ssr 필요한거 아니면 python web framework 쓰는건 멍청한 짓이다. 심지어 ssr도 node.js로 할 수 있다. ㅋㅋ 
api 이외에 용도가 하나도 없네. 상대적으로 지들도 구린거 아니까 경량화해서 api 전용으로 변했구나 싶네. 

그냥 python으로 node 체크하고 node로 웹 프레임워크 돌리는 걸로 하자 그게 맞다.

#### 2025.04.07 (2)

할 것.
1. 종료 시 쓰레드 타이밍 재정의
2. 커스텀 옵션 추가 및 적용
3. 통신 실패한 경우 예외처리 보강. 


> 강종 처리에 대한 예외 메모
```console
1.Stream connection lost: AssertionError(('_AsyncTransportBase._produce() tx buffer size underflow', -36, 1))
2.Stream connection lost: InvalidFrameError: Invalid frame received: 'Invalid FRAME_END marker
3.Scheduled callback error: ('_AsyncTransportBase._initate_abort() expected _STATE_ABORTED_BY_USER', 2)
1. ('_AsyncTransportBase._initate_abort() expected _STATE_ABORTED_BY_USER', 2)
```

#### 2025.04.07 (1)

이제 소생 잘 댐. 소켓 오류에 대해 문제는 있는데. 이제 죽어도 잘 살아남.
watcher 쓰레드가 좋아졌음.

옵션 추상화 클레스부터 작성하고 있음


#### 2025.04.03 (2)

끄아앙.. 뭔가 잘못했는데 못 찾고 있어.
뭔가 뭔가 잘못 했어

#### 2025.04.03 (1)


- 쓰레드 뻗는 문제 파악 
- 상대경로 잘라낼 정규식 문제 -> 일단 절대경로만 자르게 
- leaves 테이블 정보 컬럼 추가 해야함.
- 요청마다 robots.txt 찾지말고 가지고 있음 특정 텀 시간까진 얻은 데이터로 판단하게.
- 코드 설정 적용해야함.

![4-1.gif](./readme/4-1.png)
![4-2.gif](./readme/4-2.png)
![4-3.gif](./readme/4-3.png)

#### 2025.04.01


queue 소비를 자동 ak 해놨어서 문제가 있었는데. 이제 해결됨. 종료 후 다시 실행해도 이어서 동작함.


![3.gif](./readme/3.gif)


#### 2025.03.28 (2)


> image test1
```json
{
    "url": "https://s.pstatic.net/dthumb.phinf/?src=%22https%3A%2F%2Fhappybean-phinf.pstatic.net%2F20250212_125%2F1739350096803zkPOL_JPEG%2F%25B8%25EB%25A4%25EC312314.jpg%3Ftype%3Df464_260%22&type=nf365_240&service=navermain",
    "ext": null,
    "is_relative": false,
    "classified": "http",
    "id": null
}
```

흠흠.. selenium 부분을 좀 빨리 해야겠음.
요즘 다 js 기반이라 대다수 사이트에서 먹통임.흠흠



#### 2025.03.28 (1)


점점 의도대로 가고 있어. 가자 가자
```console
hello
db connection initialized
root updated: google
root updated: tennisreact_react_parsing_test
worker start: google
worker start: tennisreact_react_parsing_test
 [google] Received b'http://schema.org/WebPage'
 [google] Received b'https://www.google.com/imghp?hl=ko&tab=wi'
Error: Too many redirects
 [google] Received b'http://maps.google.co.kr/maps?hl=ko&tab=wl'
 [google] Received b'https://play.google.com/?hl=ko&tab=w8'
 [google] Received b'https://www.youtube.com/?tab=w1'
 [google] Received b'https://news.google.com/?tab=wn'
 [google] Received b'https://mail.google.com/mail/?tab=wm'
 [google] Received b'https://drive.google.com/?tab=wo'
 [google] Received b'https://www.google.co.kr/intl/ko/about/products?tab=wh'
 [google] Received b'http://www.google.co.kr/history/optout?hl=ko'
 [google] Received b'https://accounts.google.com/ServiceLogin?hl=ko&passive=true&continue=http://www.google.com/webhp&ec=GAZAAQ'
 [google] Received b'http://www.google.co.kr/intl/ko/services/'
 [google] Received b'http://www.google.com/setprefdomain?prefdom=KR&amp;prev=http://www.google.co.kr/&amp;sig=K_yj3Y8NgCK2GQfTVtlRpGUVV8H6I%3D'
Exiting the program.
0worker process complete: tennisreact_react_parsing_test
 worker thread signaled to stop
1 worker thread signaled to stop
watcher thread signaled to stop
Thread 1 is not alive.
worker process complete: google
bye
```

실행 및 종료.
- 필요한 것: 중복 체크, 정규식 강화, uri 아닌 것 요청 x 
![2.gif](./readme/2.gif)



#### 2025.03.27 (4)

javascript 렌더링 뒤에 로드하는 컨텐츠에 대한 것을 생각을 안했었네 ㅋㅋ 
selenium은 이전에 불법 토토 사이트 환급 비밀번호 뚫을 때 빼고는 써본적이 없네ㅋㅋ

그대로 써서 의존성을 가지던지 프로젝트 내부에 크로니움 끌어다 내장시키던지 해야겠네..


#### 2025.03.27 (3)

모델 기초 만들었고 rds 연결 및 생성 동작을 수행하고. 코드로 작성된 정보와 db 정보를 key를 토대로 통합하고
통합된 데이터를 기반으로 쓰레드를 생성하고 동작하는 기초가 거의 완성되었음.

이제 요청 및 응답 정제, pyclamd 파싱 및 스코어링
그 외 설정 저장 등. 해야 함. 


지금은 대충 이런 느낌으로.
라이브러리 사용 시 느낌도 중요하니.. 개선할 부분은 개선하는게 맞지.
```python
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




# start client example
client_start(
    db_rds_connection=rds_connection,
    db_mq_connection=rabbit_mq,
    roots=[
        Scrapper_Root('google', 'https://www.google.com', Scrapper_Root_Access_Rule(
            
            # Whether to skip duplicate URIs (If False, it may endlessly loop on a specific page.)
            skip_duplication_uri=True, 
            
            # Whether to refresh duplicate URIs (Refreshing means re-evaluating and scoring the URI.)
            refresh_duplicate_uri=True, 
            
            # Threshold count of duplicate URIs before refreshing
            refresh_duplicate_uri_count=10 
            
            )),
    ]
)
```




#### 2025.03.27 (2)

좀 잠좀 자고
sqlalchemy 모델 만들고 해야겠네.
이 라이브러리는 모델 기준으로 table 만들기가 있네 ㅋㅋ
sequelize랑 다르게 직접 만들어줄 migration 파일 만들어줄 필요가 없어서 좋네
반대로 migration 기능 자체는 없어서 외부 라이브러리에 의존하는게 좀 꼴받는데 걍 빼고 로직으로 때워야지. 그리 필요없어 보임.

최종적으로 이 기능은 데이터 더미를 얻는걸로 목적을 다 하는거니 장기적인 관리에 해당하는 기능은 필요 없음.

걍 table 없으면 만들어 쓰고 있음 그거 쓰고. 대충 버전 관리만 하면 되겠지.


#### 2025.03.27 (1)

대충 요런 느낌이 될 듯.

> source
```python


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

```

> response
```console
hello
Exiting the program.
watcher thread signaled to stop
bye
```




#### 2025.03.26

하면서 조금 기능이 점점 복합적으로 변해야할 것 같음.
pyclamd 추가해서 간단히 악성 코드를 분별함. 모든 url에 요청을 보내기 떄문.
거기에는 악의도 포함되니. 악의는 거르는게 좋음.

일단 rabbitmq에 대한 의존성을 가지기로 함.
이게 효율적인듯 


#### 2025.03.23

아직 추상화 작업 중.
다중 쓰레드의 요청을 큐 리스트를 통한 직렬 처리로 치환하여 동시성 문제를 해결.


AMQP 을 참조 가능한지 확인.. 개발 요구사항에는 필요 없는데. 그냥 단순 큐 입력만 있어도 문제 없음으로 판단.

아니면.. 그냥 rabbitMQ 또는 kafka 를 중간자에 껴서 작업량을 줄이는 것도 좋음.
직접 MQ를 구현하하는 것은 효율이 나쁜데.
사업성이 있는 작업도 아니니 코드 중량이랑 의존성을 덜어내는게 좋은지 작업량을 줄이는게 좋은지 비교할 가치가 있음. 

추후 이 코드를 사업에 이용하는 사람들을 위해선 외부 프레임워크를 사용하는게 맞고..

그렇다면 rabbitMQ, kafka 이 2개가 대세니 둘 다 사용 가능하게 의존성을 가지는게 맞나
아니면 플러그인 방식으로 입력 가능하게 인터페이스를 만들어서 쓰는게 좋아보임.
제 3의 MQ 서비스는 나올것이 분명하니.

미설정이 내부 MQ를 이용하고 
설정 시 외부 MQ를 이용하고

그럼 문제는.. 작업량이 너무 커지는데.. 흠

일단 내일은 이 부분 접어두고 데이터 요청 테스트를 해봐야지.
여기도 프록시, 다이렉트 요청 등으로 나뉠거고. 

수준을 어디까지 낮춰서 요청을 보내고 정제할껀지 목적을 보고 정해야 함..

데이터 파싱도 의존성을 가질껀지 직접 구현할껀지.. 의존성은 최소한으로 하고 싶은데.

#### 2025.03.23

![1.png](./readme/1.png)
