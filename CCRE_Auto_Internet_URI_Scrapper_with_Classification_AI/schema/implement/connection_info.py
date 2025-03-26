from ..abstract.rds.connection import CCRE_AI_Scrapper_RDS_Connection
from ..abstract.rds.predef import DatabaseType




class Connection_Info(CCRE_AI_Scrapper_RDS_Connection):
    def __init__(self):
        self._host = None
        self._password = None
        self._authentication_key_file = None
        self._port = None
        self._vhost = None
        self._database = None
        self._user = None
        self._proxy_info = None
        

    @property
    def db_type(self) -> DatabaseType:
        """
        @getter
        get db type
        """
        return self._db_type

    @db_type.setter
    def db_type(self, value: DatabaseType):
        """
        @setter
        set db type
        """
        self._db_type = value

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = value

    @property
    def authenticationKeyFile(self):
        return self._authentication_key_file

    @authenticationKeyFile.setter
    def authenticationKeyFile(self, type, value: str):
        self._authentication_key_file = {"type": type, "value": value}

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value: int):
        self._port = value

    @property
    def vhost(self):
        """
        @getter
        get vhost
        """
        return self._vhost

    @vhost.setter
    def vhost(self, value: str):
        """
        @setter
        set vhost
        """
        self._vhost = value



    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, value: str):
        self._database = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value: str):
        self._user = value

    @property
    def proxy_info(self):
        return self._proxy_info

    @proxy_info.setter
    def proxy_info(self, value):
        self._proxy_info = value