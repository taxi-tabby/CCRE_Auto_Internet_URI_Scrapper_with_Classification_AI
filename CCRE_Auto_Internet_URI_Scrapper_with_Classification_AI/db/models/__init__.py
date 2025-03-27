from sqlalchemy.orm import relationship

from .root import Roots
from .branches import Branches
from .leaves import Leaves




# Define relationships between models
Roots.branches = relationship("Branches", back_populates="root", cascade="all, delete-orphan")
Branches.root = relationship("Roots", back_populates="branches")

Branches.leaves = relationship("Leaves", back_populates="branch", cascade="all, delete-orphan")
Leaves.branch = relationship("Branches", back_populates="leaves")


# 공개할 이름 정의
__all__ = ["Roots", "Branches", "Leaves"]