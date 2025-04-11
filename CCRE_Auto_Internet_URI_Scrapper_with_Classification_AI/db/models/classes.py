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

class Classes(Base):
    """분류 테이블
    
    1. leaves 분류용 정규화 테이블 입니다
    2. 추가된 불류 값은 지워지지 않는게 좋은데..
    
    Returns:
        _type_: sqlalchemy model
    """
    __tablename__ = "classes"
    
    # 고유번호
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, type_=BigInteger)
    
    # 루트 uri
    class_code: Mapped[str] = mapped_column(type_=String(50), nullable=False)

    # 추가된 일자
    created_at: Mapped[datetime] = mapped_column(type_=DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"), nullable=False)  
    
    
    __table_args__ = (
        Index('idx_classes_class_code', 'class_code'),
    )

    def __repr__(self) -> str:
        return f"<Classes(id={self.id!r}, class_code={self.class_code!r}, created_at={self.created_at!r})>"





