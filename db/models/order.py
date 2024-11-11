from sqlalchemy.orm import relationship, Mapped, mapped_column
from litestar.contrib.sqlalchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey, DECIMAL, TEXT
from typing import TYPE_CHECKING

from .enums import OrderStatus
from uuid import UUID
if TYPE_CHECKING:
    from .user import User

class Order(UUIDAuditBase):
    __tablename__ = "order"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    address: Mapped[str] = mapped_column(TEXT, nullable=False)
    total_price: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.0)
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.PENDING)
  
    user: Mapped["User"] = relationship(back_populates="orders", lazy="selectin")
