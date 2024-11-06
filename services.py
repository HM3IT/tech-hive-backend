from typing import TYPE_CHECKING
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models import Product, Order
from repos import UserRepository, OrderRepository, ProductRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def provide_user_service(db_session: AsyncSession) -> UserRepository:
    pass
    # return UserRepository(session=db_session)


async def provide_product_service(db_session: AsyncSession) -> ProductRepository:
    pass
    # return ProductRepository(
    #     statement=select(Product)
    #         .options(
    #             selectinload(Product.category),    
    #             selectinload(Product.subcategory)  
    #         ), 
    #     session=db_session,
    # )


async def provide_order_service(db_session: AsyncSession) -> OrderRepository:
    pass
    # return OrderRepository(
    #     statement=select(Order)
    #         .options(
    #             selectinload(Order.user),         
    #             selectinload(Order.products)        
    #         ),
    #     session=db_session,
    # )
