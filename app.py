from __future__ import annotations
import os
 
from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import  SQLAlchemyPlugin

from litestar.di import Provide

from domain.users.dependencies import provide_user_service
from db.dependencies import provide_user

from domain.users.guards import oauth2_auth
from dotenv import load_dotenv
import logging 
from db.base import sqlalchemy_config, on_startup
from db.dependencies import create_collection_dependencies
from domain.users.controllers import UserController, AccessController
from domain.products.controller import ProductController
from domain.categories.controller import CategoryController, SubCategoryController
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin
from litestar.openapi.config import OpenAPIConfig

load_dotenv()
DATABASE_URI = os.environ["DATABASE_URI"]

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

openapi_config = OpenAPIConfig(
    title="My API",
    version="1.0.0",
)
 
dependencies = {
    "user_service": Provide(provide_user_service),
    "current_user": Provide(provide_user)}

dependencies.update(create_collection_dependencies())

logger.info("dependencies")
logger.info(dependencies) 

app = Litestar(
    debug=True,
    route_handlers=[UserController, AccessController, CategoryController, SubCategoryController, ProductController],
    dependencies=dependencies,
    on_startup=[on_startup],
    plugins=[SQLAlchemyInitPlugin(config=sqlalchemy_config)],
    on_app_init=[oauth2_auth.on_app_init],
    openapi_config=openapi_config,
)