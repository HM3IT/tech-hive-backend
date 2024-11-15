"""Request Token Check middleware Controllers."""

from __future__ import annotations

# import os
import logging
from litestar import Request
# from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import AbstractMiddleware
from litestar.types import Receive, Scope, Send
from db.base import AUTH_EXCLUDE_API_ROUTE
from domain.users.urls import ACCOUNT_AUTH

logger = logging.getLogger()
 
class AuthMiddleware(AbstractMiddleware):
    
    exclude = AUTH_EXCLUDE_API_ROUTE + [ACCOUNT_AUTH]
 
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        headers = Request(scope).headers
        logger.info("HEADER")
        logger.info(headers)
        api_key = headers.get("authorization")
        if not api_key:
            raise NotAuthorizedException(status_code=403, detail="Forbidden - Missing Token")

        await self.app(scope, receive, send)
