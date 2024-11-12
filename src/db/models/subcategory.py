from sqlalchemy.orm import Mapped, mapped_column, relationship
from litestar.contrib.sqlalchemy.base import UUIDBase
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING
# from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID 
if TYPE_CHECKING:
    from .category import Category

class SubCategory(UUIDBase):
    __tablename__ = "subcategory"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[UUID] = mapped_column(ForeignKey("category.id"))

    category: Mapped["Category"] = relationship(back_populates="subcategories", lazy="selectin")