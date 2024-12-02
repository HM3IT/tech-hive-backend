from __future__ import annotations

from typing import Any
from logging import getLogger
from db.models import Order, OrderProduct
from domain.repositories import OrderRepository, OrderProductRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

logger = getLogger()

class OrderService(SQLAlchemyAsyncRepositoryService[Order]):
    """Handles database operations for orders."""

    repository_type = OrderRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: OrderRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

 


class OrderProductService(SQLAlchemyAsyncRepositoryService[OrderProduct]):
    """Handles database operations for ordered products."""

    repository_type = OrderProductRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: OrderProductRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

 