from __future__ import annotations

import os
from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import autocommit_before_send_handler
from litestar import Litestar, get
from litestar.contrib.sqlalchemy.base import UUIDBase
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyPlugin

from litestar.di import Provide

from litestar.params import Parameter
from litestar.repository.filters import LimitOffset

from services import provide_user_service, provide_product_service, provide_order_service

from models import *
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.environ["DATABASE_URI"]

def provide_limit_offset_pagination(
    current_page: int = Parameter(ge=1, query="currentPage", default=1, required=False),
    page_size: int = Parameter(
        query="pageSize",
        ge=1,
        default=10,
        required=False,
    ),
) -> LimitOffset:
    """Add offset/limit pagination.

    Return type consumed by `Repository.apply_limit_offset_pagination()`.

    Parameters
    ----------
    current_page : int
        LIMIT to apply to select.
    page_size : int
        OFFSET to apply to select.
    """
    return LimitOffset(page_size, page_size * (current_page - 1))


@get("/")
async def hello_world() -> str:
    return "Hello, world!"





db_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///todo.sqlite",
    metadata=UUIDBase.metadata,
    create_all=True,
    before_send_handler=autocommit_before_send_handler,

)

app = Litestar(
    [hello_world],
    dependencies={"user_service":provide_user_service },
    plugins=[SQLAlchemyPlugin(db_config)],

)