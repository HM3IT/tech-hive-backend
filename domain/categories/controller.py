from __future__ import annotations

 
import os
from litestar import get, post, delete, patch
from litestar.exceptions import HTTPException
from litestar.controller import Controller
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from litestar.repository.filters import LimitOffset
from domain.categories.depedencies import provide_category_service
from domain.categories.services import CategoryService
from domain.categories import urls
from domain.categories.schemas import CategoryCreate, Category, CategoryUpdate
from domain.users.guards import requires_active_user, requires_superuser
from logging import getLogger
from uuid import UUID

logger = getLogger()

class CategoryController(Controller):
    """Category CRUD"""
    tags = ["Category"]
    dependencies = {"category_service": Provide(provide_category_service)}
    # guards = [requires_active_user, requires_superuser]

    @get(path=urls.CATEGORY_LIST)
    async def list_category(
        self,
        category_service: CategoryService,
        limit_offset: LimitOffset,
    ) -> OffsetPagination[Category]:
        """List Products."""
        results, total = await category_service.list_and_count(limit_offset)
        filters = [limit_offset]
        return category_service.to_schema(data=results, total=total, schema_type=Category, filters=filters)

    @post(path=urls.CATEGORY_ADD)
    async def create_category(
        self,
        category_service: CategoryService,
        data: CategoryCreate,
    ) -> Category:
        """Create a new Product."""
        category = data.to_dict()
        category_name = category["name"].strip()
   
        if len(category_name) < 0:
            raise HTTPException(detail="Please make sure to have category name",status_code=400)
        
        category_obj = await category_service.get_one_or_none(name=category_name)
        if not category_obj:
            category_obj = await category_service.create(category)

        return category_service.to_schema(data=category_obj, schema_type=Category)


    @post(path=urls.CATEGORY_EMBEDDING, guards=[requires_superuser])
    async def generate_embedding_category(
        self,
        category_service: CategoryService,
        id:UUID = Parameter(
            title="Category ID",
            description="The category to delete.",
        )
    ) -> Category:
        """Create a new Product."""
        from sentence_transformers import SentenceTransformer # loading sentence transformer inside for optimization
        
        EMBEDDING_MODEL = os.environ["EMBEDDING_MODEL"]
        embedding_model = SentenceTransformer(EMBEDDING_MODEL) 
        db_obj = await category_service.get(item_id=id)
        if not db_obj:
            raise HTTPException(detail="No such category", status_code=404)

        embedding = await category_service.generate_embedding(embedding_model=embedding_model, category=db_obj)
        logger.info(embedding)
        category_obj = await category_service.update(item_id=id, data = {"context_embedding": embedding})

        return category_service.to_schema(data=category_obj, schema_type=Category)


    @delete(path=urls.CATEGORY_REMOVE)
    async def delete_category(
        self,
        category_service: CategoryService,
        id: UUID = Parameter(
            title="Category ID",
            description="The category to delete.",
        ),
    ) -> None:
        """List Products."""
        _ = await category_service.delete(item_id=id)


    @get(path=urls.CATEGORY_DETAIL)
    async def get_category(
        self,
        category_service: CategoryService,
        id: UUID = Parameter(
            title="Product ID",
            description="The category to retrieve.",
        ),
    ) -> Category:
        """Get an existing Product."""
        obj = await category_service.get(item_id=id)
        return category_service.to_schema(data=obj,  schema_type=Category)

    @patch(
        path=urls.CATEGORY_UPDATE, guards=[requires_active_user, requires_superuser]
    )
    async def update_category(
        self,
        category_service: CategoryService,
        data: CategoryUpdate,
        id: UUID = Parameter(
            title="Category ID",
            description="The category to update.",
        ),
    ) -> Category:
        """Update an category."""
        category = data.to_dict()
        db_obj = await category_service.get(item_id=id)
        if not db_obj:
            raise HTTPException(detail="Category not found", status_code=400)
        if not category["related_context"]:
            category.pop("related_context")
        if not category["context_embedding"]:
            category.pop("context_embedding")
        logger.error(category)
        db_obj = await category_service.update(item_id=id, data=category)
        return category_service.to_schema(db_obj, schema_type=Category)

    # @delete(path=urls.PRODUCT_REMOVE, guards=[requires_superuser, requires_active_user])
    # async def delete_category(
    #     self,
    #     category_service: CategoryService,
    #     id: UUID = Parameter(
    #         title="Category ID",
    #         description="The Product to delete.",
    #     ),
    # ) -> None:
    #     """Delete a Category from the system."""
    #     await category_service.delete(item_id=id)

