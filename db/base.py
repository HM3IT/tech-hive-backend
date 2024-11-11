from __future__ import annotations

import os
from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import autocommit_before_send_handler
from litestar.contrib.sqlalchemy.plugins import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin

from dotenv import load_dotenv
from db.models.user import UUIDAuditBase 


__all__ = ["sqlalchemy_config","on_startup"]

load_dotenv()
DATABASE_URI = os.environ["DATABASE_URI"]
 

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=DATABASE_URI, session_config=session_config, before_send_handler=autocommit_before_send_handler,

) 

sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)


async def on_startup() -> None:
    """Initializes the database."""

    async with sqlalchemy_config.get_engine().begin() as conn:
        await conn.run_sync(UUIDAuditBase.metadata.create_all)

