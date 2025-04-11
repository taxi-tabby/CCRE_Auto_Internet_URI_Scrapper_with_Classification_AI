from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, Text, text
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


from .base import Base

class LeavesClass(Base):
    """리프의 적용된 식별 테이블
    
    1. 이 테이블은 특수하게 소프트 딜리트하지 않습니다.
    
    Returns:
        _type_: sqlalchemy model
    """
    __tablename__ = "leaves_classes"
    
    # 고유번호
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, type_=BigInteger)
    
    # 루트 id
    root_id: Mapped[int] = mapped_column(ForeignKey("roots.id"), nullable=False, type_=BigInteger)
    
    # 브랜치 id
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"), nullable=False, type_=BigInteger)

    # 리프 id
    leaf_id: Mapped[int] = mapped_column(ForeignKey("leaves.id"), nullable=False, type_=BigInteger)
    
    # 리프 id
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False, type_=BigInteger)
    
    # 추가된 일자
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    
    __table_args__ = (
        Index('idx_leaves_classes_default', 'root_id', 'branch_id', 'id'),
        Index('idx_leaves_classes_root', 'root_id'),
        Index('idx_leaves_classes_branch', 'branch_id'),
        Index('idx_leaves_classes_leaf', 'leaf_id'),
        Index('idx_leaves_classes_class', 'class_id'),
        Index('idx_leaves_classes_leaf_class', 'leaf_id', 'class_id'),
        Index('idx_leaves_classes_root_leaf', 'root_id', 'leaf_id'),
        Index('idx_leaves_classes_branch_leaf', 'branch_id', 'leaf_id'),
        Index('idx_leaves_classes_root_class', 'root_id', 'class_id'),
        Index('idx_leaves_classes_root_branch_leaf', 'root_id', 'branch_id', 'leaf_id'),
        Index('idx_leaves_classes_created_at', 'created_at'),  # 날짜 기반 조회용
    )
    
    def __repr__(self) -> str:
        return f"<Leaves(root_id={self.root_id!r}, branch_id={self.branch_id}, id={self.id!r}, branch_uri={self.branch_uri!r})>"





