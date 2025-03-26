import pika
import time


class PikaRabbitMQ:
    """
    ### Default rabbitMQ class to control basic rabbitMQ operations
    ### 기본적인 rabbitMQ 동작을 제어하는 클레~~~스
    - 단순 조작용으로 추상체는 없스
    """
    
    def __init__(self):
        self._connection = None
        self._channel = None
        pass
    
    def connect(self, host, port, username, password, vhost) -> bool:
        
        try:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=host,
                    port=port,
                    virtual_host=vhost,
                    credentials=pika.PlainCredentials(username, password)
                )
            )
        except RuntimeError:
            self._connection = None
        
        if self._chk_conn():
            return True
        
        return False
    
    def _chk_conn(self) -> bool:
        """
        ### Check connection
        ### 연결 오브제만 확인
        """
        if self._connection is None:
            return False
        return True
        
    def _chk_usable(self) -> bool:
        """
        ### Check connection and channel
        ### 연결과 채널을 확인
        """
        if self._connection is None or self._channel is None:
            return False
        return True
    
    
    def declare_channel(self) -> bool:
        """
        ### declares a channel for the connection
        ### 채널 생성
        """
        if not self._chk_conn():
            return False
        else:
            self._channel = self._connection.channel()
            
        if self._channel is None:
            return False
        
        return True
        
    def declare_queue(self, queue_name):
        """
        ### Declares a queue with the specified
        ### 큐 생성
        """
        if self._chk_usable():
            self._channel.queue_declare(queue=queue_name)
        
        
    def declare_exchange(self, exchange_name: str, exchange_type: str = 'direct'):
        """
        ### Declares an exchange with the specified name.
        ### 익스체인지 생성
        """
        if self._chk_usable():
            self._channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
            
        
    def bind_queue(self, exchange: str, queue_name: str, routing_key: str):
        """
        ### Binds a queue to an exchange with the specified routing key.
        ### 큐 바인딩
        """
        if self._chk_usable():
            self._channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)
            
    
    def unbind_queue(self, exchange: str, queue_name: str, routing_key: str):
        """
        ### Unbinds a queue from an exchange with the specified routing key.
        ### 큐 언바인딩
        """
        if self._chk_usable():
            self._channel.queue_unbind(exchange=exchange, queue=queue_name, routing_key=routing_key)
            
            
    def delete_queue(self, queue_name: str):
        """
        ### Deletes the specified queue.
        ### 큐 삭제
        """
        if self._chk_usable():
            self._channel.queue_delete(queue=queue_name)    
            
    def delete_exchange(self, exchange_name: str):
        """
        ### Deletes the specified exchange.
        ### 익스체인지 삭제
        """
        if self._chk_usable():
            self._channel.exchange_delete(exchange=exchange_name)
    
    
    def set_qos(self, prefetch_count: int):
        """
        ### Sets the QoS for the channel.
        ### 채널의 QoS 설정 (몇개씩 메세지를 받을지 설정)
        """
        if self._chk_usable():
            self._channel.basic_qos(prefetch_count=prefetch_count)
    
        
    def b_publish(self, exchange: str, queue_name: str, message: str | bytes):
        """
        ### Publishes a message to the specified queue.
        ### 메세지 기본 발행
        """
        if self._chk_usable():
            self._channel.basic_publish(exchange=exchange, routing_key=queue_name, body=message)
        
        
    def b_consume(self, queue_name: str, callback, delay_microseconds: int = 0):
        """
        ### Consumes a message from the specified queue with an optional delay after callback execution. 
        ### 메세지 기본 소비 (데코레이드 속도 강제 설정 포함)
        """
        def decorated_callback(ch, method, properties, body):
            callback(ch, method, properties, body)
            if delay_microseconds > 0:
                time.sleep(delay_microseconds / 1_000_000)

        if self._chk_usable():
            self._channel.basic_consume(queue=queue_name, on_message_callback=decorated_callback, auto_ack=True)
            self._channel.start_consuming()
        
        
    def close(self):
        """
        ### Closes the connections.
        ### 연결 싸그리 닫기
        """
        if self._chk_usable():
            self._channel.close()
            
        if self._chk_conn():
            self._connection.close()