from domain.categories.services import CategoryService, SubCategoryService

from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

 

async def provide_category_service(db_session: AsyncSession) -> AsyncGenerator[CategoryService, None]:

    async with CategoryService.new(
        session=db_session,
        error_messages={"duplicate_key": "This category already exists.", "integrity": "Category operation failed."},
    ) as service:
        yield service

async def provide_subcategory_service(db_session: AsyncSession) -> AsyncGenerator[SubCategoryService, None]:

    async with SubCategoryService.new(
        session=db_session,
        error_messages={"duplicate_key": "This subcategory already exists.", "integrity": "Sub-Category operation failed."},
    ) as service:
        yield service
