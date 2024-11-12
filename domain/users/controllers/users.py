"""User Account Controllers."""

from __future__ import annotations

from typing import Annotated

import logging
from litestar import Controller, Request, delete, get, patch, post
 
from litestar.params import Dependency, Parameter


from db.models import User as UserModel
from domain.users  import urls
from domain.users.guards import requires_active_user, requires_superuser
from domain.users.schemas import User, UserCreate, UserUpdate
from domain.users.services import UserService
from db.models.enums import UserType
from litestar.repository.filters import CollectionFilter

from uuid import UUID
from advanced_alchemy.service import OffsetPagination

logger = logging.getLogger()

class UserController(Controller):
    """User Account Controller."""

    tags = ["User Accounts"]
    # guards = [requires_superuser]
    dto = None
    return_dto = None

    @get(
        operation_id="ListUsers",
        name="users:list",
        summary="List Users",
        description="Retrieve the users.",
        path=urls.ACCOUNT_LIST,
        cache=60,
    )
    async def list_users(
        self,
        user_service: UserService,
        filters: Annotated[CollectionFilter, Dependency(skip_validation=True)] = None,
    ) -> OffsetPagination[User]:
        filters = filters or []
        results, total = await user_service.list_and_count(*filters)
        return user_service.to_schema(data=results, total=total, schema_type=User, filters=filters)

    @get(
        operation_id="GetUser",
        name="users:get",
        path=urls.ACCOUNT_DETAIL,
        summary="Retrieve the details of a user.",
    )
    async def get_user(
        self,
        user_service: UserService,
        user_id: Annotated[
            UUID,
            Parameter(
                title="User ID",
                description="The user to retrieve.",
            ),
        ],
    ) -> User:
        """Get a user."""
        db_obj = await user_service.get(user_id)
        return user_service.to_schema(db_obj, schema_type=User)
    
    @get(
        operation_id="AccountProfile",
        name="account:profile",
        path=urls.ACCOUNT_PROFILE,
        guards=[requires_active_user],
        summary="User Profile",
        description="User profile information.",
    )
    async def profile(self, request: Request, current_user: UserModel, user_service: UserService) -> User:
        """User Profile."""
        return user_service.to_schema(current_user, schema_type=User)


    @post(
        operation_id="CreateUser",
        name="users:create",
        summary="Create a new user.",
        cache_control=None,
        description="A user who can login and use the system.",
        path=urls.ACCOUNT_CREATE,
    )
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate,
    ) -> User:
        """Create a new user."""
        user = data.to_dict()
        if(user["is_superuser"]):
            user_type = UserType.ADMIN
        else:
            user_type = UserType.CUSTOMER

        user.update({"user_type": user_type}) 
        db_obj = await user_service.create(user)
 
        return user_service.to_schema(db_obj, schema_type=User)

    @patch(
        operation_id="UpdateUser",
        name="users:update",
        path=urls.ACCOUNT_UPDATE,
    )
    async def update_user(
        self,
        data: UserUpdate,
        user_service: UserService,
        user_id: Annotated[
            UUID,
            Parameter(
                title="User ID",
                description="The user to retrieve.",
            ),
        ],
    ) -> User:
        """Create a new user."""
        db_obj = await user_service.update(item_id=user_id, data=data.to_dict())
        return user_service.to_schema(db_obj, schema_type=User)

    @delete(
        operation_id="DeleteUser",
        name="users:delete",
        path=urls.ACCOUNT_DELETE,
        summary="Remove User",
        description="Removes a user and all associated data from the system.",
    )
    async def delete_user(
        self,
        user_service: UserService,
        user_id: Annotated[
            UUID,
            Parameter(
                title="User ID",
                description="The user to delete.",
            ),
        ],
    ) -> None:
        """Delete a user from the system."""
        logger.info("USERID")
        logger.info(user_id)
        _ = await user_service.delete(item_id = user_id)
