from __future__ import annotations
import os
 
from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import  SQLAlchemyPlugin

from litestar.di import Provide

from domain.users.dependencies import provide_user_service

from domain.users.guards import oauth2_auth
from dotenv import load_dotenv
import logging 
from db.base import db_config
from db.dependencies import create_collection_dependencies
from domain.users.controllers import UserController, AccessController

from litestar.openapi.config import OpenAPIConfig

load_dotenv()
DATABASE_URI = os.environ["DATABASE_URI"]

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
# logging.getLogger("sqlalchemy.orm").setLevel(logging.DEBUG)

openapi_config = OpenAPIConfig(
    title="My API",
    version="1.0.0",
)
 
dependencies = {"user_service": Provide(provide_user_service)}
dependencies.update(create_collection_dependencies())

logger.info("dependencies")
logger.info(dependencies) 

app = Litestar(
    debug=True,
    route_handlers=[UserController, AccessController],
    dependencies=dependencies,
    plugins=[SQLAlchemyPlugin(db_config)],
    on_app_init=[oauth2_auth.on_app_init],
    openapi_config=openapi_config,
)