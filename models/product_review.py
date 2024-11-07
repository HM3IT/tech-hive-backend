from sqlalchemy.orm import Mapped, mapped_column
from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey, DECIMAL, TEXT

class ProductReview(UUIDAuditBase):
    __tablename__ = "product_review"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    rating: Mapped[float] = mapped_column(DECIMAL(2, 1))
    review_text: Mapped[str] = mapped_column(TEXT)