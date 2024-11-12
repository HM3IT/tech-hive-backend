from sqlalchemy.orm import selectinload

from db.models import Product
from domain.products.services import ProductService

from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

 

async def provide_product_service(db_session: AsyncSession) -> AsyncGenerator[ProductService, None]:

    async with ProductService.new(
        session=db_session,
        load=[selectinload(Product.category), selectinload(Product.product_reviews)],
        error_messages={"duplicate_key": "This user already exists.", "integrity": "User operation failed."},
    ) as service:
        yield service

 