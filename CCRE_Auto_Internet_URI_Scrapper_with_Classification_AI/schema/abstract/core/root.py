from abc import ABC, abstractmethod

from ..rds.sqlalchemy import CCRE_AI_Scrapper_RDS_Connection_SQLAlchemy
from .access_rule import CCRE_AI_Scrapper_Access_Rule

class CCRE_AI_Scrapper_Root(ABC):
    """
    root는 여러게일 가능성이 있으며, 각 뿌리에서 동시에 데이터를 수집합니다.
    root는 실행되는 쓰레드의 단위가 됩니다.
    """



    # @property
    # @abstractmethod
    # def rds_db_connection(self):
    #     """
    #     각 root의 이름을 반환합니다.
    #     이는 프로그램 실행 시 등록된 키를 비교하여 없는 경우 루트를 db에 등록합니다.
    #     """
    #     pass

    # @rds_db_connection.setter
    # @abstractmethod
    # def rds_db_connection(self, value: CCRE_AI_Scrapper_RDS_Connection_SQLAlchemy):
    #     raise NotImplementedError



    @property
    @abstractmethod
    def root_key(self):
        """
        각 root의 이름을 반환합니다.
        이는 프로그램 실행 시 등록된 키를 비교하여 없는 경우 루트를 db에 등록합니다.
        """
        raise NotImplementedError

    @root_key.setter
    @abstractmethod
    def root_key(self, value: str):
        raise NotImplementedError





    @property
    @abstractmethod
    def root_uri(self):
        """
        시작 지점의 uri 입니다
        이 uri를 기반으로 접근 가능한 모든 uri를 수집합니다.
        
        uri는 특수한 포멧(변수)을 지정 가능합니다 (ex: https://www.naver.com/{page})
        """
        raise NotImplementedError

    @root_uri.setter
    @abstractmethod
    def root_uri(self, value: str):
        raise NotImplementedError
    


    @property
    @abstractmethod
    def access_rule(self)->CCRE_AI_Scrapper_Access_Rule:
        """
        접근 규칙 설정
        """
        raise NotImplementedError

    @access_rule.setter
    @abstractmethod
    def access_rule(self, value: CCRE_AI_Scrapper_Access_Rule):
        raise NotImplementedError
    
