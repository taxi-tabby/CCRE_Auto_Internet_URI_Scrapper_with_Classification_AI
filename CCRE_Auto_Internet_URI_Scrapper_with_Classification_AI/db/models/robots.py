
from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import BigInteger, DateTime, Integer, ForeignKey, Text, text, Index
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base

class Robots(Base):
    """로봇 테이블
    
    1. robots.txt 파일을 파싱하여 저장하는 테이블입니다.
    
    Returns:
        _type_: sqlalchemy model
    """
    __tablename__ = "robots"
    
    # 고유번호
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, type_=Integer)
    
    # 루트 uri
    base_domain: Mapped[str] = mapped_column(type_=String(255), nullable=False)
    
    # 규칙 JSON
    ruleset_text: Mapped[str] = mapped_column(type_=Text, nullable=False, default="")
    
    # 추가된 일자
    created_at: Mapped[datetime] = mapped_column(type_=DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"), nullable=False)  
    
    # 마지막 수정 일자
    updated_at: Mapped[datetime] = mapped_column(type_=DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"), nullable=False)  
    
    
    __table_args__ = (
        Index('default_robots_index', 'base_domain'),
    )
    
    def __repr__(self) -> str:
        return f"<Robots(id={self.id!r}, base_domain={self.base_domain!r}, created_at={self.created_at!r})>"





