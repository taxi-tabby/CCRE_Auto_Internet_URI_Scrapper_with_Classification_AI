from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import BigInteger, Boolean, DateTime, Integer, ForeignKey, Text, text, Index
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import INTEGER as SQLiteInteger


from .base import LocalBase

class LocalSlaves(LocalBase):
    """하위 노드 정보 테이블
                
    Returns:
        _type_: sqlalchemy model
    """
    __tablename__ = "local_slaves"
    

    # 고유번호
    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(SQLiteInteger, "sqlite"), 
        primary_key=True, 
        autoincrement=True
    )
    
    # 디스커버 참조성 아이디 (다른 db에 있음음로 외래키 설정 불가)
    service_discover_id: Mapped[int] = mapped_column(type_=Integer, nullable=False)
    
    # 추가된 일자
    created_at: Mapped[datetime] = mapped_column(type_=DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"), nullable=False)  

    __table_args__ = (
        Index('idx_local_slaves_service_discover_id_unique', 'service_discover_id', unique=True),
    )
    
    
    def __repr__(self) -> str:
        return f"<LocalSlaves(id={self.id!r}, service_discover_id={self.service_discover_id!r})>"




