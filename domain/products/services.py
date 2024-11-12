from __future__ import annotations

from typing import Any  
from db.models import Product
from domain.repositories import ProductRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService


 
class ProductService(SQLAlchemyAsyncRepositoryService[Product]):
    """Handles database operations for products."""

    repository_type = ProductRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: ProductRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    
 