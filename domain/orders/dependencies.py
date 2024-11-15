# from typing import TYPE_CHECKING
# from sqlalchemy import select
# from sqlalchemy.orm import selectinload

# from db.models import Product, Order
# from domain.repositories import UserRepository, OrderRepository, ProductRepository

# from sqlalchemy.ext.asyncio import AsyncSession



# async def provide_order_service(db_session: AsyncSession) -> OrderRepository:
#     return OrderRepository(
#         statement=select(Order)
#             .options(
#                 selectinload(Order.user),         
#                 selectinload(Order.products)        
#             ),
#         session=db_session,
#     )
