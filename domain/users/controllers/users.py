"""User Account Controllers."""

from __future__ import annotations

from typing import Annotated

from uuid import UUID
from logging import getLogger

from litestar import Controller, Request, Response, delete, get, patch, post
from litestar.params import Dependency, Parameter
from litestar.repository.filters import CollectionFilter

from domain.users  import urls
from domain.users.guards import requires_active_user, requires_superuser
from domain.users.schemas import User, UserCreate, UserUpdate
from domain.users.services import UserService

from db.models import User as UserModel
from db.models.enums import UserType

from advanced_alchemy.service import OffsetPagination

logger = getLogger()

class UserController(Controller):
    """User Account Controller."""

    tags = ["User Accounts"]
    
    @get(
        operation_id="ListUsers",
        name="users:list",
        summary="List Users",
        description="Retrieve the users.",
        path=urls.ACCOUNT_LIST,
        guards = [requires_active_user, requires_superuser],
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
        guards = [requires_active_user, requires_superuser],
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
        summary="User Profile",
        description="User profile information.",
        guards = [requires_active_user],
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
        # temporarily disable guards
        # guards = [requires_active_user, requires_superuser],
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
        guards = [requires_active_user],
    )
    async def update_user(
        self,
        data: UserUpdate,
        user_service: UserService,
        current_user:UserModel
    ) -> Response:
        """Create a new user."""
        user_info = data.to_dict()
        logger.info("CATACH user data")
        logger.info(user_info)
        old_password = user_info.get("old_password")
        if not old_password:
            return Response(content={"message":"Original Password must be included"}, status_code=401)


        # Authentication check    
        user_obj = await user_service.authenticate(email=current_user.email, password= old_password)
        if not user_obj:
             return Response(content={"message":"Wrong Password or email"}, status_code=401)
            
        # Update old password
        new_password = user_info.get("new_password")
        # optmization for password and must has legnth at least 8
        if new_password and (new_password != old_password and len(new_password) > 8):
            update_password_dict = {
                "current_password": old_password,
                "new_password": new_password
            }
            user_obj = await user_service.update_password(data=update_password_dict,db_obj=user_obj)
 
        address = user_info.get("new_address")
        image_url = user_info.get("new_image_url")
        name = user_info.get("new_name")

        if (address and len(address) > 0) or (image_url and len(image_url) > 0) or (name and len(name) >0):
            user_dict = {}
            if address:
                user_dict.update({"address": address})
            if image_url:
                user_dict.update({"image_url": image_url})
            if name:
                user_dict.update({"name": name})

            logger.info("UPDATE DICT")
            logger.info(user_dict)
            user_obj = await user_service.update(item_id= current_user.id, data=user_dict)
        return Response(content={"message":"Successfully updated"}, status_code=200)

    @delete(
        operation_id="DeleteUser",
        name="users:delete",
        path=urls.ACCOUNT_DELETE,
        summary="Remove User",
        description="Removes a user and all associated data from the system.",
        guards = [requires_active_user, requires_superuser],
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
