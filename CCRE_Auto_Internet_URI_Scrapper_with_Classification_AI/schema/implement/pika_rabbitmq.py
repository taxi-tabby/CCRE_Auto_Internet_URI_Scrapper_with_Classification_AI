import pika
import time

import pika.channel
import pika.spec


class PikaRabbitMQ:
    """
    ### Default rabbitMQ class to control basic rabbitMQ operations
    ### 기본적인 rabbitMQ 동작을 제어하는 클레~~~스
    - 단순 조작용으로 추상체는 없스
    """
    

    
    def __init__(self, name: str):
        self._connection = None
        self._channel = None
        self._closed_flag = False
        self._connection_params = None
        self.name = name

    def connect(self, host, port, username, password, vhost) -> bool:
        try:
            self._connection_params = {
                "host": host,
                "port": port,
                "username": username,
                "password": password,
                "vhost": vhost,
            }
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=host,
                    port=port,
                    virtual_host=vhost,
                    credentials=pika.PlainCredentials(username, password),
                    socket_timeout=None,
                    blocked_connection_timeout=30,
                    heartbeat=5,
                    client_properties={'connection_name': 'CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI'},
                )
            )
        except pika.exceptions.AMQPConnectionError as e:
            self._connection = None
        except Exception as e:
            self._connection = None

        if self._chk_conn():
            return True

        return False

    def reconnect(self) -> bool:
        """
        ### Reconnects to RabbitMQ by cleaning up all resources and retrying.
        ### 모든 리소스를 정리하고 재연결 시도
        """
        if self._connection_params is None:
            return False

        # Clean up existing connection and channel
        if self._chk_usable() and self._channel.is_open:
            self._channel.close()
        if self._chk_conn() and self._connection.is_open:
            self._connection.close()

        self._channel = None
        self._connection = None
        self._closed_flag = False

        # Retry connection
        return self.connect(
            self._connection_params["host"],
            self._connection_params["port"],
            self._connection_params["username"],
            self._connection_params["password"],
            self._connection_params["vhost"],
        )
    
    
    
    def _chk_channel(self) -> bool:
        """
        ### Check channel
        ### 채널만 확인
        """
        if self._channel is None or not self._channel.is_open:
            return False
        return True
    
    def _chk_conn(self) -> bool:
        """
        ### Check connection
        ### 연결 오브제만 확인
        """
        if self._connection is None or not self._connection.is_open:
            return False
        return True
        
    def _chk_usable(self) -> bool:
        """
        ### Check connection and channel
        ### 연결과 채널을 확인
        """
        if self._connection is None or not self._connection.is_open or self._channel is None or not self._channel.is_open:
            return False
        return True


    def declare_channel(self) -> bool:
        """
        ### Declares a channel for the connection if not already created.
        ### 채널 생성 (이미 있는 경우 생성하지 않음)
        """
        if not self._chk_conn():
            return False
        
        if self._channel is not None:
            print("Channel already exists")
            return True
        
        self._channel = self._connection.channel()
        
        if self._channel is None:
            return False
        
        return True
        
     
    def declare_queue(self, queue_name, durable=False, exclusive=False, auto_delete=False, arguments=None):
        """
        ### Declares a queue with the specified name and options.
        ### 큐 생성 (상세 옵션 포함)
        - `durable`: 큐가 서버 재시작 후에도 유지되도록 설정 (기본 False)
        - `exclusive`: 해당 큐가 연결에만 사용되고, 연결이 종료되면 삭제되도록 설정 (기본 False)
        - `auto_delete`: 소비자가 없으면 큐가 자동으로 삭제되도록 설정 (기본 False)
        - `arguments`: 추가적인 큐 설정 파라미터 (기본 None)
        """
        if self._chk_usable():
            self._channel.queue_declare(
                queue=queue_name,
                durable=durable,
                exclusive=exclusive,
                auto_delete=auto_delete,
                arguments=arguments,
            )
        else:
            print("connection or channel is not usable")
            
            
    
    def declare_exchange(self, exchange_name: str, exchange_type: str = 'direct', durable=False, auto_delete=False, arguments=None):
        """
        ### Declares an exchange with the specified name and options.
        ### 익스체인지 생성 (상세 옵션 포함)
        - `exchange_type`: 익스체인지 유형 (기본 'direct')
        - `durable`: 익스체인지가 서버 재시작 후에도 유지되도록 설정 (기본 False)
        - `auto_delete`: 소비자가 없으면 익스체인지가 자동으로 삭제되도록 설정 (기본 False)
        - `arguments`: 추가적인 익스체인지 설정 파라미터 (기본 None)
        """
        if self._chk_usable():
            self._channel.exchange_declare(
                exchange=exchange_name,
                exchange_type=exchange_type,
                durable=durable,
                auto_delete=auto_delete,
                arguments=arguments
            )
        else:
            print("connection or channel is not usable")
    
    def bind_queue(self, exchange: str, queue_name: str, routing_key: str, arguments=None):
        """
        ### Binds a queue to an exchange with the specified routing key and options.
        ### 큐 바인딩 (상세 옵션 포함)
        - `arguments`: 바인딩 설정에 추가적인 파라미터
        """
        if self._chk_usable():
            self._channel.queue_bind(
                exchange=exchange,
                queue=queue_name,
                routing_key=routing_key,
                arguments=arguments
            )
        else:
            print("connection or channel is not usable")
    
    def unbind_queue(self, exchange: str, queue_name: str, routing_key: str):
        """
        ### Unbinds a queue from an exchange with the specified routing key.
        ### 큐 언바인딩
        """
        if self._chk_usable():
            self._channel.queue_unbind(exchange=exchange, queue=queue_name, routing_key=routing_key)
        else:
            print("connection or channel is not usable")
            
    def delete_queue(self, queue_name: str):
        """
        ### Deletes the specified queue.
        ### 큐 삭제
        """
        if self._chk_usable():
            self._channel.queue_delete(queue=queue_name)    
        else:
            print("connection or channel is not usable")
            
            
    def delete_exchange(self, exchange_name: str):
        """
        ### Deletes the specified exchange.
        ### 익스체인지 삭제
        """
        if self._chk_usable():
            self._channel.exchange_delete(exchange=exchange_name)
        else:
            print("connection or channel is not usable")
    
    def set_qos(self, prefetch_count: int):
        """
        ### Sets the QoS for the channel.
        ### 채널의 QoS 설정 (몇개씩 메세지를 받을지 설정)
        """
        if self._chk_usable():
            self._channel.basic_qos(prefetch_count=prefetch_count)
        else:
            print("connection or channel is not usable")
        
        
        
    def b_publish(self, exchange: str, routing_key: str, message: str | bytes, properties: pika.BasicProperties = None):
        """
        ### Publishes a message to the specified queue.
        ### 메세지 기본 발행
        """
        if self._chk_usable():
            
            if properties is None:
                properties = pika.BasicProperties(delivery_mode=2)
                
            self._channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message, properties=properties, )
            
        else:
            print("connection or channel is not usable")
        
        
        
    def b_consume(self, queue_name: str, callback, delay_sec: int = 0):
        """
        Consumes a message from the specified queue with an optional delay after callback execution.
        """
        
        # Required function for dispatching messages to user, having the signature:
        # on_message_callback(channel, method, properties, body)
        # - channel: BlockingChannel
        # - method: spec.Basic.Deliver
        # - properties: spec.BasicProperties
        # - body: bytes
        def decorated_callback(ch: pika.channel.Channel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes) -> None:
            
            def close():
                if self._closed_flag:
                    print(f"Consumer is closed. Stopping message consumption. ch: {ch.channel_number}")
                    ch.stop_consuming()
                    
                   
            callback(ch, method, properties, body)
            
            # Optional delay after callback execution
            if delay_sec > 0:
                # print(f"Delaying message acknowledgment for {delay_sec} seconds...")
                time.sleep(delay_sec)
            
            # After delay, acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            close()

            
        
        #--------------------------------------------------------
        # Check if connection and channel are usable before consuming messages
        #--------------------------------------------------------
        if self._chk_usable():
            # Disable auto_ack (set to False) to handle acknowledgment manually
            self._channel.basic_consume(queue=queue_name, on_message_callback=decorated_callback, auto_ack=False, consumer_tag=queue_name, exclusive=False,)
            self._channel.start_consuming()
        else:
            print("Connection or channel is not usable.")
        
        
    
    def force_channel_consuming_stop(self):
        """
        ### Forcefully stops consuming messages from the channel.
        ### 채널에서 메세지 소비 강제 중지
        """
        if self._chk_channel():
            self._channel.stop_consuming()
        else:
            print("connection or channel is not usable")
        
    def stop_consuming(self):
        """
        ### Stops consuming messages from the queue.
        ### 메세지 소비 중지
        """
        if self._chk_channel():
            # self._channel.stop_consuming()
            self._closed_flag = True
        else:
            print("connection or channel is not usable")
        
        
    def close(self):
        """
        ### Closes the connections.
        ### 연결 싸그리 닫기
        """
        if self._chk_usable():
            self._channel.close()
            
        if self._chk_conn():
            self._connection.close()