from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.models import Product
from domain.repositories import ProductRepository

from sqlalchemy.ext.asyncio import AsyncSession



async def provide_product_service(db_session: AsyncSession) -> ProductRepository:
    return ProductRepository(
        statement=select(Product)
            .options(
                selectinload(Product.category),    
                selectinload(Product.subcategory)  
            ), 
        session=db_session,
    )
