from __future__ import annotations

from typing import Any  
from db.models import Category, SubCategory
from domain.repositories import CategoryRepository, SubCategoryRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService


 
class CategoryService(SQLAlchemyAsyncRepositoryService[Category]):
    """Handles database operations for products' categories."""

    repository_type = CategoryRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: CategoryRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    
class SubCategoryService(SQLAlchemyAsyncRepositoryService[SubCategory]):
    """Handles database operations for products' subcategories."""

    repository_type = SubCategoryRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: SubCategoryRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type
