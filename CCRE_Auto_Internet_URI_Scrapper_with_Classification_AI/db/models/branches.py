from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, Text, text
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base

class Branches(Base):
    """브렌치 테이블
    
    Returns:
        _type_: sqlalchemy model
    """
    __tablename__ = "branches"
    
    # 고유번호
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, type_=BigInteger)
    
    # 부모 브랜치 id
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("branches.id"), nullable=True, type_=BigInteger)
    # parent_id: Mapped[Optional[int]] = mapped_column(nullable=True, type_=Integer, default=None)
    
    # 루트 id
    root_id: Mapped[int] = mapped_column(ForeignKey("roots.id"), nullable=False, type_=BigInteger)
    
    # 브랜치에서 검색할 uri
    branch_uri: Mapped[str] = mapped_column(type_=Text, nullable=False)
    
    # 중복 검색 횟수
    _duplicate_count: Mapped[int] = mapped_column(type_=Integer, default=0)
    
    # 추가된 일자
    created_at: Mapped[datetime] = mapped_column(type_=DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)  
    
    # 인덱스 설정
    __table_args__ = (
        Index('idx_branches_default', 'root_id', 'id'),
        Index('idx_branches_uri', 'branch_uri'),
        Index('idx_branches_root_id', 'root_id'),
        Index('idx_branches_parent_id', 'root_id', 'parent_id'),
    )
    
    
    def __repr__(self) -> str:
        return f"<Branches(root_id={self.root_id!r}, id={self.id!r}, branch_uri={self.branch_uri!r})>"





