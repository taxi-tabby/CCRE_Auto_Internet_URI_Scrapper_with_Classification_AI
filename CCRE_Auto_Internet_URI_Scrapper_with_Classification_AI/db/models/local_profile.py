from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import BigInteger, DateTime, Integer, ForeignKey, Text, text, Index
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import INTEGER as SQLiteInteger


from .base import LocalBase

class LocalProfile(LocalBase):
    """로컬 기타 값 저장용 테이블
                
    Returns:
        _type_: sqlalchemy model
    """
    __tablename__ = "local_profile"
    

    
    # 고유번호
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, type_=Integer)
    
    # 루트 고유 지정 키
    data_key: Mapped[str] = mapped_column(type_=String(255), nullable=False)
    
    # 루트 uri
    data_value: Mapped[str] = mapped_column(type_=Text, nullable=False)

    # 추가된 일자
    created_at: Mapped[datetime] = mapped_column(type_=DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"), nullable=False)  
    

    __table_args__ = (
        Index('idx_local_profile_key_uri', 'data_key', 'created_at'),
    )
    
    
    def __repr__(self) -> str:
        return f"<LocalProfile(id={self.id!r}, data_key={self.data_key!r}, data_value={self.data_value!r})>"





