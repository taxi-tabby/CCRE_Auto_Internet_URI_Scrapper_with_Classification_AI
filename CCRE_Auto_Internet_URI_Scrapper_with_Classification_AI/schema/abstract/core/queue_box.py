from abc import ABC, abstractmethod
from .queue_message import CCRE_AI_Scrapper_QueueMessage as messageObject



class CCRE_AI_Scrapper_QueueBox(ABC):
    """
    Message queue abstact class
    """
    
    """
    queue list
    """
    _queue: list[messageObject] = []
    
    @abstractmethod
    def message_index_of(self, message: messageObject) -> (int):
        """
        큐에서 메세지의 순서를 반환함
        없으면 -1을 반환함
        """
        raise NotImplementedError


    @abstractmethod
    def enqueue(self, message: messageObject) -> (bool):
        """
        메세지를 큐에 추가함
        """
        raise NotImplementedError

    @abstractmethod
    def dequeue(self, message: messageObject) -> (bool):
        """
        메세지를 큐에서 제거함.
        """
        raise NotImplementedError

    @abstractmethod
    def has_next(self) -> (bool):
        """
        다음 메세지가 있는지 확인
        """
        raise NotImplementedError

    @abstractmethod
    def size(self) -> (int):
        """
        큐의 길이를 정수로 반환
        """
        raise NotImplementedError