from sqlalchemy.orm import relationship

from .roots import Roots
from .branches import Branches
from .leaves import Leaves
from .robots import Robots
from .classes import Classes
from .leave_classes import LeavesClass
from .service_discover import ServiceDiscover

from .local_profile import LocalProfile
from .local_slaves import LocalSlaves

# ================================================================================================
# 데이터베이스 모델 간의 관계 정의
# ================================================================================================

# ------------------------------------------------------------------------------------------------
# Roots(루트) <-> Branches(브랜치) 관계
# - 한 루트는 여러 브랜치를 가질 수 있음 (1:N)
# - 브랜치가 삭제되면 해당 브랜치의 하위 항목들도 함께 삭제됨 (cascade)
# ------------------------------------------------------------------------------------------------
Roots.branches = relationship("Branches", back_populates="root", cascade="all, delete-orphan")
Branches.root = relationship("Roots", back_populates="branches")



# ------------------------------------------------------------------------------------------------
# Branches(브랜치) <-> Leaves(리프) 관계
# - 한 브랜치는 여러 리프를 가질 수 있음 (1:N)
# - 리프가 삭제되면 해당 리프의 하위 항목들도 함께 삭제됨 (cascade)
# ------------------------------------------------------------------------------------------------
Branches.leaves = relationship("Leaves", back_populates="branch", cascade="all, delete-orphan")
Leaves.branch = relationship("Branches", back_populates="leaves")




# ------------------------------------------------------------------------------------------------
# Leaves(리프) <-> Classes(클래스) 관계
# - 리프와 클래스는 다대다(M:N) 관계를 가짐
# - 연결 테이블: leaves_classes
# ------------------------------------------------------------------------------------------------
Leaves.classes = relationship("Classes", secondary="leaves_classes", backref="leaf_classes")




# ------------------------------------------------------------------------------------------------
# Roots(루트) <-> Robots(로봇) 관계
# - 한 루트는 여러 로봇 규칙을 가질 수 있음 (1:N)
# - 로봇이 삭제되면 해당 로봇의 하위 항목들도 함께 삭제됨 (cascade)
# ------------------------------------------------------------------------------------------------
# Robots.root = relationship("Roots", back_populates="robots")
# Roots.robots = relationship("Robots", back_populates="root")






# ------------------------------------------------------------------------------------------------
# LeavesClass(리프클래스) 관계 정의
# - LeavesClass는 리프와 클래스의 다대다 관계를 위한 연결 테이블
# - 각 테이블과의 관계를 명시적으로 정의
# ------------------------------------------------------------------------------------------------
LeavesClass.root = relationship("Roots", foreign_keys=[LeavesClass.root_id])
LeavesClass.branch = relationship("Branches", foreign_keys=[LeavesClass.branch_id])
LeavesClass.leaf = relationship("Leaves", foreign_keys=[LeavesClass.leaf_id], overlaps="classes,leaf_classes")
LeavesClass.class_item = relationship("Classes", foreign_keys=[LeavesClass.class_id], overlaps="classes,leaf_classes")


# 공개할 이름 정의
__all__ = ["Roots", "Branches", "Leaves", "Robots", "Classes", "LeavesClass", "LocalProfile", "ServiceDiscover", "LocalSlaves"]