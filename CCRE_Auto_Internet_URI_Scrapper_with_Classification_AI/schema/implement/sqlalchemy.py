from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.abstract.rds.predef import DatabaseType
from ..abstract.rds.sqlalchemy import CCRE_AI_Scrapper_RDS_Connection_SQLAlchemy
from .connection_info import Connection_Info
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class SQLAlchemyConnection(CCRE_AI_Scrapper_RDS_Connection_SQLAlchemy):
    def __init__(self):
        self._connection = None
        self._engine = None
        self._session_local = None

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, value: Connection_Info):
        self._connection = value
        self._initialize_engine()
        
        
        
    def get_db(self):
        if not self._session_local:
            raise ValueError("SessionLocal is not initialized. Ensure the connection is set.")
        
        db = self._session_local()
        try:
            yield db
        finally:
            db.close()


    def _build_connection_url(self):
        """
        ### Constructs the connection URL based on the database type and connection info.
        ### 연결 스키마 만드는데 사용됨.
        """
        if self._connection.db_type == "sqlite3" or self._connection.db_type == DatabaseType.SQLITE3:
            return f"sqlite:///{self._connection.database}"
        elif self._connection.db_type == "postgresql" or self._connection.db_type == DatabaseType.POSTGRESQL:
            return f"postgresql://{self._connection.user}:{self._connection.password}@{self._connection.host}:{self._connection.port}/{self._connection.database}"
        else:
            raise ValueError(f"Unsupported database type: {self._connection.db_type}")


    def _initialize_engine(self):
        if not self._connection:
            raise ValueError("Connection object is not set.")
        
        connection_url = self._build_connection_url()
        self._engine = create_engine(connection_url)
        self._session_local = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)


    def close(self):
        """
        Closes the engine and releases any resources held by it.
        """
        if self._engine:
            self._engine.dispose()
            self._engine = None
            self._session_local = None
