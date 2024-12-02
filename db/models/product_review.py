from typing import TYPE_CHECKING
from uuid import UUID

from litestar.contrib.sqlalchemy.base import UUIDAuditBase

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DECIMAL, TEXT

if TYPE_CHECKING:
    from .product import Product
 

class ProductReview(UUIDAuditBase):
    __tablename__ = "product_review"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("product.id"), nullable=False)
    rating: Mapped[float] = mapped_column(DECIMAL(2, 1))
    review_text: Mapped[str] = mapped_column(TEXT)
    product: Mapped["Product"] = relationship(back_populates="product_reviews")
  