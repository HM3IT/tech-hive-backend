from sqlalchemy.orm import Mapped, mapped_column, relationship
from litestar.contrib.sqlalchemy.base import UUIDAuditBase
from sqlalchemy import Integer, ForeignKey, DECIMAL, String
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models import Product
    from .order import Order

class OrderProduct(UUIDAuditBase):
    __tablename__ = "order_product"
 
    product_id: Mapped[UUID] = mapped_column(ForeignKey("product.id"), nullable=False)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("order.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_at_order: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    discount_percent_at_order: Mapped[float] = mapped_column(DECIMAL(5, 2), default=0.0)
    product: Mapped["Product"] = relationship(back_populates="order_products")    
    order: Mapped["Order"] = relationship("Order", back_populates="order_products")
 