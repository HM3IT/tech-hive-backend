# from sqlalchemy.orm import Mapped, mapped_column
# from advanced_alchemy.base import UUIDAuditBase
# from sqlalchemy import Integer, ForeignKey, DECIMAL
# from uuid import UUID

# class OrderProduct(UUIDAuditBase):
#     __tablename__ = "order_product"
 
#     product_id: Mapped[UUID] = mapped_column(ForeignKey("product.id"), nullable=False)
#     order_id: Mapped[UUID] = mapped_column(ForeignKey("order.id"), nullable=False)
#     quantity: Mapped[int] = mapped_column(Integer, nullable=False)
#     price_at_order: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
