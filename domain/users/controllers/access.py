"""User Account Controllers."""

from __future__ import annotations

from typing import Annotated
from logging import getLogger

from litestar import Controller, Request, Response, post
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar.security.jwt import OAuth2Login

from domain.users import urls
from domain.users.guards import oauth2_auth
from domain.users.services import UserService
from domain.users.schemas import AccountLogin, AccountRegister, User, APIAuth

logger = getLogger()

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
        data: Annotated[AccountLogin, Body(title="OAuth2 Login", media_type=RequestEncodingType.JSON)],
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
        user_service: UserService,
        data: AccountRegister,
    ) -> Response[AccountLogin]:
        """User Signup."""
        user_data = data.to_dict()
        user = await user_service.create(user_data)
        if not user:
            return Response(content={"message": "Failed to Signup"}, status_code=500)
        user = await user_service.authenticate(data.email, data.password)
        return oauth2_auth.login(user.email)
 