from __future__ import annotations
import os
 
import logging 
from dotenv import load_dotenv

from litestar import Litestar
from litestar.di import Provide
from litestar.config.cors import CORSConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin

from domain.tags.controller import TagController
from domain.orders.controller import OrderController
from domain.users.dependencies import provide_user_service
from domain.categories.controller import CategoryController
from domain.statistics.controller import StatisticController
from domain.users.controllers import UserController, AccessController
from domain.products.controller import ProductController, ProductReviewController
 
from domain.middleware import AuthMiddleware
from domain.users.guards import oauth2_auth

from db.base import sqlalchemy_config, on_startup
from db.dependencies import create_collection_dependencies, provide_user
 
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
    "current_user": Provide(provide_user)
}

dependencies.update(create_collection_dependencies())

cors_config = CORSConfig(allow_origins=["*"])

app = Litestar(
    debug=True,
    route_handlers=[UserController, AccessController, CategoryController, TagController, ProductController, OrderController, StatisticController, ProductReviewController],
    dependencies=dependencies,
    on_startup=[on_startup],
    cors_config=cors_config,
    plugins=[SQLAlchemyInitPlugin(config=sqlalchemy_config)],
    # middleware=[AuthMiddleware],
    on_app_init=[oauth2_auth.on_app_init],
    openapi_config=openapi_config,
)