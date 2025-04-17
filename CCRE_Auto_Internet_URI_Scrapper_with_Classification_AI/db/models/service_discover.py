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


from .base import Base

class ServiceDiscover(Base):
    """등록된 서비스를 관리하는 테이블
                
    Returns:
        _type_: sqlalchemy model
    """
    __tablename__ = "service_discover"
    

    
    # 고유번호
    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(SQLiteInteger, "sqlite"), 
        primary_key=True, 
        autoincrement=True
    )
    
    # 유니크 명칭
    unique_id: Mapped[str] = mapped_column(type_=String(24), nullable=False)
    
    # 활성화 여부
    is_active: Mapped[bool] = mapped_column(type_=Boolean(), nullable=False, default=False)
    
    # 루트 고유 지정 키
    guild_token: Mapped[str] = mapped_column(type_=String(512), nullable=False)
    
    
    address_outer_ip: Mapped[str] = mapped_column(type_=String(64), nullable=False, unique=False, default='')
    address_inner_ip: Mapped[str] = mapped_column(type_=String(64), nullable=False, unique=False, default='')
    address_mac: Mapped[str] = mapped_column(type_=String(64), nullable=False, unique=False, default='')
    
    
    # 추가된 일자
    created_at: Mapped[datetime] = mapped_column(type_=DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"), nullable=False)  
    
    # 마지막 활성화 일자
    last_active_at: Mapped[datetime] = mapped_column(type_=DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"), nullable=False)  
    
    
    
    
    __table_args__ = (
        Index('idx_service_discover_default_search', 'unique_id', 'guild_token', unique=True),
        Index('idx_service_discover_unique_id', 'unique_id'),
        Index('idx_service_discover_is_active', 'is_active'),
        Index('idx_service_discover_guild_token', 'guild_token'),
    )
    
    
    def __repr__(self) -> str:
        return f"<ServiceDiscover(id={self.id!r}, unique_id={self.unique_id!r}, guild_token={self.guild_token!r})>"




