"""User Account Controllers."""

from __future__ import annotations

from typing import Annotated

from advanced_alchemy.utils.text import slugify
from litestar import Controller, Request, Response, get, post
from litestar.di import Provide
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar.security.jwt import OAuth2Login

from db.models import User as UserModel
from domain.users import urls
from domain.users.guards import oauth2_auth, requires_active_user
from domain.users.schemas import AccountLogin, AccountRegister, User, APIAuth
from domain.users.services import UserService
import logging

logger = logging.getLogger()

class AccessController(Controller):
    """User login and registration."""

    tags = ["Access"]
    signature_namespace = {
        "OAuth2Login": OAuth2Login,
        "RequestEncodingType": RequestEncodingType,
        "Body": Body,
        "User": User,
    }

    @post(
        operation_id="AccountLogin",
        name="account:login",
        path=urls.ACCOUNT_LOGIN,
        cache=False,
        summary="Login",
        exclude_from_auth=True,
    )
    async def login(
        self,
        user_service: UserService,
        data: Annotated[AccountLogin, Body(title="OAuth2 Login", media_type=RequestEncodingType.URL_ENCODED)],
    ) -> Response[OAuth2Login]:
        """Authenticate a user."""
        user = await user_service.authenticate(data.email, data.password)
        return oauth2_auth.login(user.email)

    @post(
        operation_id="AccountAuth",
        name="account:auth",
        path=urls.ACCOUNT_AUTH,
        cache=False,
        summary="API endpoint authorization",
        exclude_from_auth=True,
    )
    async def api_authorized(
        self,
        user_service: UserService,
        data: Annotated[APIAuth, Body(title="OAuth2 Login", media_type=RequestEncodingType.URL_ENCODED)],
    ) -> Response[OAuth2Login]:
        """Authenticate a user."""
        user = await user_service.authenticate(data.username, data.password)
        return oauth2_auth.login(user.email)
    @post(
        operation_id="AccountLogout",
        name="account:logout",
        path=urls.ACCOUNT_LOGOUT,
        cache=False,
        summary="Logout",
        exclude_from_auth=True,
    )
    async def logout(
        self,
        request: Request,
    ) -> Response:
        """Account Logout"""
        request.cookies.pop(oauth2_auth.key, None)
        request.clear_session()

        response = Response(
            {"message": "OK"},
            status_code=200,
        )
        response.delete_cookie(oauth2_auth.key)

        return response

    @post(
        operation_id="AccountRegister",
        name="account:register",
        path=urls.ACCOUNT_REGISTER,
        cache=False,
        summary="Create User",
        description="Register a new account.",
    )
    async def signup(
        self,
        request: Request,
        user_service: UserService,
        data: AccountRegister,
    ) -> User:
        """User Signup."""
        user_data = data.to_dict()
        user = await user_service.create(user_data)
        return user_service.to_schema(user, schema_type=User)

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
