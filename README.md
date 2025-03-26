# CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI


### dependency:
- sqlalchemy (data storage)
- pika (rabbitmq)
- pyclamd (codesniff check)



### ref
https://huggingface.co/





### devlog

#### 2025.03.27

대충 요런 느낌이 될 듯.
```python


from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.module import client_start
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.connection_info import Connection_Info
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.abstract.rds.predef import DatabaseType

rds_connection = Connection_Info()
rds_connection.db_type = DatabaseType.SQLITE3
rds_connection.database = "test.db"

client_start(
    db_connection=rds_connection,
    roots=[]
)

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
