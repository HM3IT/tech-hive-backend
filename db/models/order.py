from typing import TYPE_CHECKING

from uuid import UUID
from .enums import OrderStatus

from litestar.contrib.sqlalchemy.base import UUIDAuditBase

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, DECIMAL, TEXT, String

if TYPE_CHECKING:
    from .user import User
    from .order_product import OrderProduct

class Order(UUIDAuditBase):
    __tablename__ = "order"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    address: Mapped[str] = mapped_column(TEXT, nullable=False)
    phone: Mapped[str] = mapped_column(String(100), nullable=False)
    total_price: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.0)
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.PENDING)
    expected_arrived_date:Mapped["str"] = mapped_column(String, nullable=True, default=None)
    order_products: Mapped[list["OrderProduct"]] = relationship(back_populates="order", lazy="selectin")
    handler_id: Mapped[str] = mapped_column(String(150),nullable=True)

    user: Mapped["User"] = relationship(back_populates="orders", lazy="selectin")
