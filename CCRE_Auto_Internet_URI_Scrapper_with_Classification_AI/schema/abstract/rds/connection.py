from abc import ABC, abstractmethod
from .predef import ConnectionAuthenticationFileType, ConnectionAuthenticationFileObject
from typing import NamedTuple

class CCRE_AI_Scrapper_RDS_Connection(ABC):
    """
    engine을 create 하기 위한 connection schema text를 정의합니다.
    """

    @property
    @abstractmethod
    def host(self):
        """
        @getter
        get host domain or ip address
        """
        pass

    @host.setter
    @abstractmethod
    def host(self, value: str):
        """
        @setter
        set host domain or ip address
        """
        pass

    @property
    @abstractmethod
    def password(self):
        """
        @getter
        get password
        """
        pass

    @password.setter
    @abstractmethod
    def password(self, value: str) -> dict:
        """
        @setter
        set password
        """
        pass
    
    @property
    @abstractmethod
    def authenticationKeyFile(self) -> ConnectionAuthenticationFileObject:
        """
        @getter
        get authenticationKeyFile
        """
        pass

    @authenticationKeyFile.setter
    @abstractmethod
    def authenticationKeyFile(self, type: ConnectionAuthenticationFileType, value: str):
        """
        @setter
        set authenticationKeyFile
        """
        pass

    @property
    @abstractmethod
    def port(self):
        """
        @getter
        get port number
        """
        pass

    @port.setter
    @abstractmethod
    def port(self, value: int):
        """
        @setter
        set port number
        """
        pass

    @property
    @abstractmethod
    def database(self):
        """
        @getter
        get database name
        """
        pass

    @database.setter
    @abstractmethod
    def database(self, value: str):
        """
        @setter
        set database name
        """
        pass

    @property
    @abstractmethod
    def user(self):
        """
        @getter
        get user name
        """
        pass

    @user.setter
    @abstractmethod
    def user(self, value: str):
        """
        @setter
        set user name
        """
        pass

    @property
    @abstractmethod
    def proxy_info(self):
        """
        @getter
        get proxy information
        type : CCRE_AI_Scrapper_RDS_Connection
        """
        pass

    @proxy_info.setter
    @abstractmethod
    def proxy_info(self, value: 'CCRE_AI_Scrapper_RDS_Connection'):
        """
        @setter
        set proxy information
        """
        pass
