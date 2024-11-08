from __future__ import annotations

import os
from dotenv import load_dotenv
from typing import TYPE_CHECKING, Any

from litestar.exceptions import PermissionDeniedException
from litestar.security.jwt import OAuth2PasswordBearerAuth

from db.base import db_config

from db.models import User
from domain.users import urls
from domain.users.dependencies import provide_user_service
import logging
 
from litestar.connection import ASGIConnection
from litestar.handlers.base import BaseRouteHandler
from litestar.security.jwt import Token


__all__ = ("current_user_from_token","requires_active_user" ,"oauth2_auth","requires_superuser")
# __all__ = ("requires_superuser", "requires_active_user", "requires_verified_user", "current_user_from_token", "auth")

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")

def requires_active_user(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    """Request requires active user.

    Verifies the request user is active.

    Args:
        connection (ASGIConnection): HTTP Request
        _ (BaseRouteHandler): Route handler

    Raises:
        PermissionDeniedException: Permission denied exception
    """
    if connection.user.is_active:
        return
    msg = "Inactive account"
    raise PermissionDeniedException(msg)


def requires_superuser(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    """Request requires active superuser.

    Args:
        connection (ASGIConnection): HTTP Request
        _ (BaseRouteHandler): Route handler

    Raises:
        PermissionDeniedException: Permission denied exception

    Returns:
        None: Returns None when successful
    """
    if connection.user.is_superuser:
        return
    raise PermissionDeniedException(detail="Insufficient privileges")


# def requires_verified_user(connection: ASGIConnection, _: BaseRouteHandler) -> None:
#     """Verify the connection user is a superuser.

#     Args:
#         connection (ASGIConnection): Request/Connection object.
#         _ (BaseRouteHandler): Route handler.

#     Raises:
#         PermissionDeniedException: Not authorized

#     Returns:
#         None: Returns None when successful
#     """
#     if connection.user.is_verified:
#         return
#     raise PermissionDeniedException(detail="User account is not verified.")


async def current_user_from_token(token: Token, connection: ASGIConnection[Any, Any, Any, Any]) -> User | None:
    """Lookup current user from local JWT token.

    Fetches the user information from the database


    Args:
        token (str): JWT Token Object
        connection (ASGIConnection[Any, Any, Any, Any]): ASGI connection.


    Returns:
        User: User record mapped to the JWT identifier
    """
    user_service = await anext(provide_user_service(db_config.provide_session(connection.app.state, connection.scope)))
    user = await user_service.get_one_or_none(email=token.sub)
    return user if user and user.is_active else None


oauth2_auth = OAuth2PasswordBearerAuth[User](
    retrieve_user_handler=current_user_from_token,
    token_secret=SECRET_KEY,
    token_url=urls.ACCOUNT_LOGIN,
    exclude=[
        urls.ACCOUNT_LOGIN,
        urls.ACCOUNT_REGISTER,
        urls.ACCOUNT_CREATE,
        "/schema",
        "/tests"
    ],
)
