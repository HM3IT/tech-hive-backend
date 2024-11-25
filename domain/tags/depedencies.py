from domain.tags.services import TagService, ProductTagService

from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator


async def provide_tag_service(db_session: AsyncSession) -> AsyncGenerator[TagService, None]:

    async with TagService.new(
        session=db_session,
        error_messages={"duplicate_key": "This Tag already exists.", "integrity": "Tag operation failed."},
    ) as service:
        yield service


async def provide_product_tag_service(db_session: AsyncSession) -> AsyncGenerator[ProductTagService, None]:

    async with ProductTagService.new(
        session=db_session,
        error_messages={"duplicate_key": "This product with that tag already exists.", "integrity": "Tag to Product operation failed."},
    ) as service:
        yield service