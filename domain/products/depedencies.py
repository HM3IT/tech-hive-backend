from sqlalchemy.orm import selectinload

from db.models import Product, ProductReview
from domain.products.services import ProductService, ProductReviewService

from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

 

async def provide_product_service(db_session: AsyncSession) -> AsyncGenerator[ProductService, None]:

    async with ProductService.new(
        session=db_session,
        load=[selectinload(Product.category), selectinload(Product.product_reviews)],
        error_messages={"duplicate_key": "This user already exists.", "integrity": "User operation failed."},
    ) as service:
        yield service

async def provide_product_review_service(db_session: AsyncSession) -> AsyncGenerator[ProductReviewService, None]:

    async with ProductReviewService.new(
        session=db_session,
        load=[selectinload(ProductReview.product), ],
        error_messages={"duplicate_key": "This user has already give review to this product.", "integrity": "Product review operation failed."},
    ) as service:
        yield service

 