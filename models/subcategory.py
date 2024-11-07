from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.base import UUIDBase
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product
    from .category import Category

class SubCategory(UUIDBase):
    __tablename__ = "subcategory"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))

    products: Mapped[list["Product"]] = relationship(back_populates="subcategory", lazy="selectin")
    category: Mapped["Category"] = relationship(back_populates="subcategories", lazy="selectin")