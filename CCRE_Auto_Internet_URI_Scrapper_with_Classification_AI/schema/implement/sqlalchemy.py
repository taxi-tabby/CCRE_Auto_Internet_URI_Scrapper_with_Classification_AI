from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.abstract.rds.predef import DatabaseType
from ..abstract.rds.sqlalchemy import CCRE_AI_Scrapper_RDS_Connection_SQLAlchemy
from .connection_info import Connection_Info
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid

from contextlib import contextmanager
from typing import Generator
from sqlalchemy.orm import Session

class SQLAlchemyConnection(CCRE_AI_Scrapper_RDS_Connection_SQLAlchemy):
    def __init__(self):
        self._connection = None
        self._engine = None
        self._session_local = None
        self._connection_id = str(uuid.uuid4())  # 각 인스턴스에 고유 ID 부여
        
    @property
    def connection_id(self):
        """이 연결의 고유 ID를 반환합니다."""
        return self._connection_id
    
    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, value: Connection_Info):
        self._connection = value
        self._initialize_engine()
        
    @property
    def engine(self):
        """엔진 인스턴스 반환"""
        return self._engine
        
    @contextmanager
    def get_db(self) -> Generator[Session, None, None]:
        """데이터베이스 세션을 생성하고 반환하며, 작업이 끝나면 세션을 닫는 컨텍스트 매니저."""
        if not self._session_local:
            raise ValueError(f"Connection {self._connection_id}: SessionLocal is not initialized. Ensure the connection is set.")
        
        db: Session = self._session_local()  # db 세션을 Session 타입으로 명시
        try:
            yield db  # db 세션 반환
        finally:
            db.close()  # 세션 종료

    def _build_connection_url(self):
        """
        ### Constructs the connection URL based on the database type and connection info.
        ### 연결 스키마 만드는데 사용됨.
        """
        if self._connection.db_type == "sqlite3" or self._connection.db_type == DatabaseType.SQLITE3:
            # SQLite에서는 각 연결이 독립적이도록 메모리 모드일 때 고유 식별자 추가
            if self._connection.database == ':memory:':
                return f"sqlite:///{self._connection.database}?cache=shared&uri=true&check_same_thread=False"
            return f"sqlite:///{self._connection.database}?check_same_thread=False"
        elif self._connection.db_type == "postgresql" or self._connection.db_type == DatabaseType.POSTGRESQL:
            return f"postgresql://{self._connection.user}:{self._connection.password}@{self._connection.host}:{self._connection.port}/{self._connection.database}"
        else:
            raise ValueError(f"Connection {self._connection_id}: Unsupported database type: {self._connection.db_type}")

    def _initialize_engine(self):
        if not self._connection:
            raise ValueError(f"Connection {self._connection_id}: Connection object is not set.")
        
        connection_url = self._build_connection_url()
        
        # 엔진 생성 시 고유성을 보장하기 위한 설정 추가
        self._engine = create_engine(
            connection_url,
            # 각 엔진에 고유한 이름 할당
            pool_pre_ping=True,  # 연결 검증
            connect_args={"application_name": f"app-{self._connection_id}"} if self._connection.db_type == DatabaseType.POSTGRESQL else {}
        )
        
        self._session_local = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        print(f"Connection {self._connection_id} initialized with {self._connection.db_type} database")

    def close(self):
        """
        Closes the engine and releases any resources held by it.
        """
        if self._engine:
            print(f"Closing connection {self._connection_id}")
            self._engine.dispose()
            self._engine = None
            self._session_local = None
            
    def __del__(self):
        """인스턴스가 소멸될 때 자동으로 연결을 닫습니다."""
        self.close()