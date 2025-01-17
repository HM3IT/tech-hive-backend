from __future__ import annotations

import os
from dotenv import load_dotenv

from db.models.user import UUIDAuditBase 

from domain.users import urls
from domain.products import urls as product_urls
from domain.categories import urls as category_urls

from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import autocommit_before_send_handler
from litestar.contrib.sqlalchemy.plugins import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin


__all__ = ["sqlalchemy_config","on_startup", "AUTH_EXCLUDE_API_ROUTE"]

load_dotenv()
DATABASE_URI = os.environ["DATABASE_URI"]
 
AUTH_EXCLUDE_API_ROUTE:list[str] =[
    urls.ACCOUNT_LOGIN,
    urls.ACCOUNT_REGISTER,
    urls.ACCOUNT_CREATE,
    category_urls.CATEGORY_LIST, 
    product_urls.PRODUCT_ADVANCED_SEARCH,
    r"^/api/products/(list|trend|detail/[^/]+)$",
    r"^/api/tags/(list|detail/[^/]+)$",
    r"^/api/files/(?!upload$|update/)[^/]+$",
    "^/schema",
    "^/tests"
]

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=DATABASE_URI, 
    session_config=session_config,
    before_send_handler=autocommit_before_send_handler,
) 

sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)

async def on_startup() -> None:
    """Initializes the database."""

    async with sqlalchemy_config.get_engine().begin() as conn:
        await conn.run_sync(UUIDAuditBase.metadata.create_all)

