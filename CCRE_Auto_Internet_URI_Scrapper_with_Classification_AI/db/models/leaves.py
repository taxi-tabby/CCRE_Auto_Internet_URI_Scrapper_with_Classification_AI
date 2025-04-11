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

class Leaves(Base):
    """리프 테이블
    
    Returns:
        _type_: sqlalchemy model
    """
    __tablename__ = "leaves"
    
    # 고유번호
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, type_=BigInteger)
    
    # 루트 id
    root_id: Mapped[int] = mapped_column(ForeignKey("roots.id"), nullable=False, type_=BigInteger)
    
    # 브랜치 id
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"), nullable=False, type_=BigInteger)
    
    # 식별된 데이터 문자열
    # val_classified: Mapped[str] = mapped_column(type_=Text, nullable=False)
    
    # 따로 테이블 분리할까 했는데. 너무 과하게 쪼개는것도 문제라서..
    # 그냥 여기서 처리함.
    val_html_meta_title: Mapped[Optional[str]] = mapped_column(type_=Text, nullable=True) #html 의 title 태그의 내용
    val_html_meta_og_title: Mapped[Optional[str]] = mapped_column(type_=Text, nullable=True) #html 의 meta 태그 중 og:title 의 내용
    val_html_meta_robots: Mapped[Optional[str]] = mapped_column(type_=Text, nullable=True) #html 의 meta 태그 중 robots 의 내용
    val_html_meta_description: Mapped[Optional[str]] = mapped_column(type_=Text, nullable=True) #html 의 meta 태그 중 description 의 내용
    val_html_meta_keywords: Mapped[Optional[str]] = mapped_column(type_=Text, nullable=True) #html 의 meta 태그 중 keywords 의 내용
    val_html_meta_author: Mapped[Optional[str]] = mapped_column(type_=Text, nullable=True) #html 의 meta 태그 중 author 의 내용
    
    # MIME 타입
    val_mime_type: Mapped[Optional[str]] = mapped_column(type_=Text, nullable=True) 
    
    # 메인 언어
    val_main_language: Mapped[Optional[str]] = mapped_column(type_=Text, nullable=True) 
    
    # 콘텐츠 사이즈
    val_content_size: Mapped[Optional[int]] = mapped_column(type_=Integer, nullable=True)
    
    # 링크 카운트
    # 해당 uri에서 발견된 링크의 갯수
    link_cnt: Mapped[int] = mapped_column(type_=Integer, nullable=False, default=0)
    
    
    # 추가된 일자
    created_at: Mapped[datetime] = mapped_column(type_=DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)  
    
    
    __table_args__ = (
        Index('idx_leaves_root_branch_id', 'root_id', 'branch_id', 'id'),
    )
    
    
    
    def __repr__(self) -> str:
        return f"<Leaves(root_id={self.root_id!r}, branch_id={self.branch_id}, id={self.id!r}, branch_uri={self.branch_uri!r})>"





