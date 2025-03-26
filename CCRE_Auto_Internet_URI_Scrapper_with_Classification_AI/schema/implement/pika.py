import pika



class pikaRabbitMQ:
    """
    기본적인 rabbitMQ 동작을 제어하는 클레~~~스
    """
    
    def __init__(self):
        self._connection = None
        self._channel = None
        pass
    
    def connect(self, host, port, username, password, vhost):
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
                virtual_host=vhost,
                credentials=pika.PlainCredentials(username, password)
            )
        )
        
    
    def _chk_conn(self) -> bool:
        """
        Check connection
        """
        if self._connection is None:
            return False
        return True
        
    def _chk_usable(self) -> bool:
        """
        Check connection and channel
        """
        if self._connection is None or self._channel is None:
            return False
        return True
    
    
    def declare_channel(self) -> bool:
        """
        declares a channel for the connection
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
        Declares a queue with the specified
        """
        if self._chk_usable():
            self._channel.queue_declare(queue=queue_name)
        
        
    def b_publish(self, exchange: str, queue_name: str, message: str | bytes):
        """
        Publishes a message to the specified queue.
        """
        if self._chk_usable():
            self._channel.basic_publish(exchange=exchange, routing_key=queue_name, body=message)
        
        
    def b_consume(self, queue_name: str, callback):
        """
        Consumes a message from the specified queue.
        """
        if self._chk_usable():
            self._channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            self._channel.start_consuming()
        
        
    def close(self):
        """
        Closes the connections.
        """
        if self._chk_usable():
            self._channel.close()
            
        if self._chk_conn():
            self._connection.close()