from sqlalchemy.orm import relationship, Mapped, mapped_column
from litestar.contrib.sqlalchemy.base import UUIDBase
from sqlalchemy import String, Integer, ForeignKey, DECIMAL, TEXT
from typing import TYPE_CHECKING
# from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID 
if TYPE_CHECKING:
    from .category import Category
    from .product_review import ProductReview 

class Product(UUIDBase):
    __tablename__ = "product"
    
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(TEXT)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    discount_percent: Mapped[float] = mapped_column(DECIMAL(5, 2), default=0.0)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    sub_image_url: Mapped[dict] = mapped_column(nullable=True, default={})
    brand: Mapped[str] = mapped_column(String(150), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    sold: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
 
    category_id: Mapped[UUID] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(back_populates="products", lazy="selectin")

    product_reviews: Mapped[list["ProductReview"]] = relationship(back_populates="product", lazy="selectin", cascade="delete, all")
    
    @property
    def category_name(self) -> str|None:
        return self.category.name if self.category else None