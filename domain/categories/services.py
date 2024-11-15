from __future__ import annotations

from typing import Any, TYPE_CHECKING
from db.models import Category, SubCategory
from domain.repositories import CategoryRepository, SubCategoryRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer
 
class CategoryService(SQLAlchemyAsyncRepositoryService[Category]):
    """Handles database operations for products' categories."""

    repository_type = CategoryRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: CategoryRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    async def generate_embedding(self, embedding_model:SentenceTransformer, category: Category) -> list[float]:
        text = category.related_context
        if not text:
            return [0.00] 
        return embedding_model.encode(text).tolist()

    
class SubCategoryService(SQLAlchemyAsyncRepositoryService[SubCategory]):
    """Handles database operations for products' subcategories."""

    repository_type = SubCategoryRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: SubCategoryRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type
