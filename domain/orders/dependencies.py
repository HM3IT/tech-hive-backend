from sqlalchemy.orm import selectinload

from db.models import Order, OrderProduct
from domain.orders.services import OrderService, OrderProductService

from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

async def provide_order_service(db_session: AsyncSession) -> AsyncGenerator[OrderService, None]:

    async with OrderService.new(
        session=db_session,
        load=[
            selectinload(Order.user), 
            selectinload(Order.order_products)
        ],
        error_messages={"duplicate_key": "This order already exists.", "integrity": "Order operation failed."},
    ) as service:
        yield service

async def provide_ordered_product_service(db_session: AsyncSession) -> AsyncGenerator[OrderProductService, None]:

    async with OrderProductService.new(
        session=db_session,
        load=[selectinload(OrderProduct.product)],
        error_messages={"duplicate_key": "This Ordered Product already exists.", "integrity": "Order product operation failed."},
    ) as service:
        yield service
