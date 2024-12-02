
from db.models import User

from domain.users.services import UserService

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from collections.abc import AsyncGenerator

async def provide_user_service(db_session: AsyncSession) -> AsyncGenerator[UserService, None]:
    """Construct repository and service objects for the request."""
    async with UserService.new(
        session=db_session,
        load=[selectinload(User.orders)],
     error_messages={"duplicate_key": "This user already exists.", "integrity": "User operation failed."},
    ) as service:
        yield service
