from __future__ import annotations

import os
from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import autocommit_before_send_handler
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig

from dotenv import load_dotenv
from db.models import *


__all__ = ["db_config"]

load_dotenv()
DATABASE_URI = os.environ["DATABASE_URI"]

db_config = SQLAlchemyAsyncConfig(
    connection_string=DATABASE_URI,
    create_all=True,
    before_send_handler=autocommit_before_send_handler,
)


