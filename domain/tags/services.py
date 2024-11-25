from __future__ import annotations

from typing import Any
from db.models import Tags, ProductTags
from domain.repositories import TagRepository, ProductTagRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

 
    
class TagService(SQLAlchemyAsyncRepositoryService[Tags]):
    """Handles database operations for products' Tags."""

    repository_type = TagRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: TagRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type


class ProductTagService(SQLAlchemyAsyncRepositoryService[ProductTags]):
    """Handles database operations for ProductTags."""

    repository_type = ProductTagRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: ProductTagRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type
