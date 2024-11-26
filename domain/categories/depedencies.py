from domain.categories.services import CategoryService

from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

 

async def provide_category_service(db_session: AsyncSession) -> AsyncGenerator[CategoryService, None]:

    async with CategoryService.new(
        session=db_session,
        error_messages={"duplicate_key": "This category already exists.", "integrity": "Category operation failed."},
    ) as service:
        yield service
