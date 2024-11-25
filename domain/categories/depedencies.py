from domain.categories.services import CategoryService, TagService

from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

 

async def provide_category_service(db_session: AsyncSession) -> AsyncGenerator[CategoryService, None]:

    async with CategoryService.new(
        session=db_session,
        error_messages={"duplicate_key": "This category already exists.", "integrity": "Category operation failed."},
    ) as service:
        yield service

async def provide_tag_service(db_session: AsyncSession) -> AsyncGenerator[TagService, None]:

    async with TagService.new(
        session=db_session,
        error_messages={"duplicate_key": "This Tag already exists.", "integrity": "Tag operation failed."},
    ) as service:
        yield service
