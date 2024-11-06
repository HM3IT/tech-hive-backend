# from sqlalchemy.orm import relationship, Mapped, mapped_column
# from advanced_alchemy.base import UUIDBase
# from sqlalchemy import String
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from .product import Product
#     from .subcategory import SubCategory

# class Category(UUIDBase):
#     __tablename__ = "category"
    
#     name: Mapped[str] = mapped_column(String(255), nullable=False)
#     products: Mapped[list["Product"]] = relationship(back_populates="category", lazy="selectin")
#     subcategories: Mapped[list["SubCategory"]] = relationship(back_populates="category", lazy="selectin")
