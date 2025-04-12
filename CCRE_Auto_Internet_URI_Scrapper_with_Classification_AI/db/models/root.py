from typing import List
from typing import Optional
from sqlalchemy import BigInteger, Integer, ForeignKey, Text, text, Index
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base

class Roots(Base):
    """루트 테이블
                
    Returns:
        _type_: sqlalchemy model
    """
    __tablename__ = "roots"
    

    
    # 고유번호
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, type_=BigInteger)
    
    # 루트 고유 지정 키
    root_key: Mapped[str] = mapped_column(type_=String(255), nullable=False)
    
    # 루트 uri
    root_uri: Mapped[str] = mapped_column(type_=Text, nullable=False)
    
    # 규칙 JSON
    rules: Mapped[str] = mapped_column(type_=Text, nullable=False)
    
    __table_args__ = (
        Index('idx_roots_key_uri', 'root_key', 'root_uri'),
    )
    
    
    def __repr__(self) -> str:
        return f"<Roots(id={self.id!r}, root_key={self.root_key!r}, root_uri={self.root_uri!r})>"





