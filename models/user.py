from __future__ import annotations

from sqlalchemy.orm import relationship, Mapped, mapped_column
from litestar.contrib.sqlalchemy.base import UUIDAuditBase
from sqlalchemy import String, DECIMAL, TEXT
from typing import TYPE_CHECKING
from datetime import date, datetime
from .enums import UserType, CustomerLevel

if TYPE_CHECKING:
    from .order import Order

class User(UUIDAuditBase):
    __tablename__ = "user"
    
    username: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    email: Mapped[str] = mapped_column(String(255), index=True, unique=True, nullable=False)
    address: Mapped[str] = mapped_column(TEXT)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str] = mapped_column(TEXT)
    user_type: Mapped[UserType] = mapped_column(default=UserType.CUSTOMER)
    user_level: Mapped[CustomerLevel] = mapped_column(default=CustomerLevel.CLASSIC)
    total_spent: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.0)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    verified_at: Mapped[date] = mapped_column(nullable=True, default=None)
    orders: Mapped[list["Order"]] = relationship(back_populates="user", lazy="selectin")
