from __future__ import annotations

import os
from dotenv import load_dotenv
from litestar import Litestar, get
from litestar.contrib.sqlalchemy.base import UUIDBase
# from litestar.contrib.sqlalchemy.plugins import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin
from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyPlugin

from litestar.di import Provide
from litestar.params import Parameter
from litestar.repository.filters import LimitOffset
from advanced_alchemy.base import orm_registry
load_dotenv()
DB_URI = os.environ["DB_URI"]

# def provide_limit_offset_pagination(
#     current_page: int = Parameter(ge=1, query="currentPage", default=1, required=False),
#     page_size: int = Parameter(
#         query="pageSize",
#         ge=1,
#         default=10,
#         required=False,
#     ),
# ) -> LimitOffset:
#     """Add offset/limit pagination.

#     Return type consumed by `Repository.apply_limit_offset_pagination()`.

#     Parameters
#     ----------
#     current_page : int
#         LIMIT to apply to select.
#     page_size : int
#         OFFSET to apply to select.
#     """
#     return LimitOffset(page_size, page_size * (current_page - 1))

@get("/")
async def hello_world() -> str:
    return "Hello, world!"
 
 

config = SQLAlchemyAsyncConfig(
    connection_string=DB_URI, create_all=True, metadata=orm_registry.metadata, 
)
 
plugin = SQLAlchemyPlugin(config=config)
app = Litestar(
    route_handlers=[hello_world],
    plugins=[plugin],
    # dependencies={"limit_offset": Provide(provide_limit_offset_pagination)},
)