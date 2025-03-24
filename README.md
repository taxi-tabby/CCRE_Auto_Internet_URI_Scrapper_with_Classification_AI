# CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI


### dependency:
- sqlalchemy



### ref
https://huggingface.co/



### devlog


#### 2025.03.23

아직 추상화 작업 중.
다중 쓰레드의 요청을 큐 리스트를 통한 직렬 처리로 치환하여 동시성 문제를 해결.


AMQP 을 참조 가능한지 확인.. 개발 요구사항에는 필요 없는데. 그냥 단순 큐 입력만 있어도 문제 없음으로 판단.

#### 2025.03.23

![1.png](./readme/1.png)
