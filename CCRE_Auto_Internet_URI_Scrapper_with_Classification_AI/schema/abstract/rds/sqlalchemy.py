from abc import ABC, abstractmethod
from .connection import CCRE_AI_Scrapper_RDS_Connection as connectionObject

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# # Database configuration
# DATABASE_URL = "sqlite:///./database.db"  # Replace with your database URL

# # Create the database engine
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# # Create a configured "Session" class
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Dependency to get a database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


class CCRE_AI_Scrapper_RDS_Connection_SQLAlchemy(ABC):
    """
    추상화 객체!
    schema text를  CCRE_AI_Scrapper_RDS_Connection 인스턴스를 받아서 생성합니다.
    """

    @property
    def connection_id(self):
        """이 연결의 고유 ID를 반환합니다."""
        pass

    @property
    @abstractmethod
    def connection(self):
        pass

    @connection.setter
    @abstractmethod
    def connection(self, value: connectionObject):
        pass


    @abstractmethod
    def get_db(self, rds_connection_object: connectionObject) -> None:
        """
        CCRE_AI_Scrapper_RDS_Connection 인스턴스를 받아서 처리합니다.
        """
        pass