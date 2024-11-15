from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import relationship, Mapped, mapped_column
from litestar.contrib.sqlalchemy.base import UUIDBase
from sqlalchemy import String, Text, Float
from sqlalchemy.dialects.postgresql import ARRAY

if TYPE_CHECKING:
    from .product import Product
    from .subcategory import SubCategory

class Category(UUIDBase):
    __tablename__ = "category"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    products: Mapped[list["Product"]] = relationship(back_populates="category", lazy="selectin")
    related_context: Mapped[str]= mapped_column(Text, nullable=True)
    context_embedding: Mapped[Optional[list[float]]] = mapped_column(ARRAY(Float), nullable=True)
