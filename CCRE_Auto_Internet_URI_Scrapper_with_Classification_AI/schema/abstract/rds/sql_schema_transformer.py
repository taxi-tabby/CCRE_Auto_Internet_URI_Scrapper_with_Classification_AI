from abc import ABC, abstractmethod
from .connection import CCRE_AI_Scrapper_RDS_Connection as connectionObject

class CCRE_AI_Scrapper_RDS_Connection_Transformer(ABC):
    """
    추상화 객체!
    schema text를  CCRE_AI_Scrapper_RDS_Connection 인스턴스를 받아서 생성합니다.
    """

    @property
    @abstractmethod
    def connection(self):
        pass

    @connection.setter
    @abstractmethod
    def connection(self, value: connectionObject):
        pass


    @abstractmethod
    def transform(self, rds_connection_object: connectionObject) -> None:
        """
        CCRE_AI_Scrapper_RDS_Connection 인스턴스를 받아서 처리합니다.
        """
        pass