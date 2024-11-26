from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship, Mapped, mapped_column
from litestar.contrib.sqlalchemy.base import UUIDBase
from sqlalchemy import String, Text, ForeignKey

from uuid import UUID

if TYPE_CHECKING:
    from .product import Product


class Tags(UUIDBase):
    __tablename__ = "tags"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True, default="")
    products: Mapped[list["ProductTags"]] = relationship(back_populates="tag", lazy="selectin")


class ProductTags(UUIDBase):
    __tablename__ = "product_tags"
    
    product_id: Mapped[UUID] = mapped_column(ForeignKey("product.id"), nullable=False)
    tag_id: Mapped[UUID] = mapped_column(ForeignKey("tags.id"), nullable=False)
    
    tag: Mapped["Tags"] = relationship(back_populates="products", lazy="selectin")
    product: Mapped["Product"] = relationship(back_populates="product_tags", lazy="selectin")
