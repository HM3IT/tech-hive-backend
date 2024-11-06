from sqlalchemy.orm import relationship, Mapped, mapped_column
from litestar.contrib.sqlalchemy.base import UUIDAuditBase
from sqlalchemy import String, DECIMAL, TEXT
from typing import TYPE_CHECKING

from .enums import UserType, CustomerLevel

# if TYPE_CHECKING:
#     from .order import Order

class User(UUIDAuditBase):
    __tablename__ = "user"
    
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    address: Mapped[str] = mapped_column(TEXT)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str] = mapped_column(TEXT)
    user_type: Mapped[UserType] = mapped_column(default=UserType.CUSTOMER)
    user_level: Mapped[CustomerLevel] = mapped_column(default=CustomerLevel.CLASSIC)
    total_spent: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.0)

    # orders: Mapped[list["Order"]] = relationship(back_populates="user", lazy="selectin")

