from __future__ import annotations

from typing import TYPE_CHECKING

from litestar import get, post, delete, patch
from litestar.exceptions import HTTPException
from litestar.controller import Controller
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from litestar.repository.filters import LimitOffset
from domain.categories.depedencies import provide_category_service, provide_subcategory_service
from domain.categories.services import CategoryService, SubCategoryService
from domain.categories import urls
from domain.categories.schemas import CategoryCreate, Category, SubCategory
from domain.users.guards import requires_active_user, requires_superuser

from uuid import UUID

class CategoryController(Controller):
    """Category CRUD"""
    tags = ["Category"]
    dependencies = {"category_service": Provide(provide_category_service)}

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

    @post(path=urls.CATEGORY_ADD, guards=[requires_superuser, requires_active_user])
    async def create_category(
        self,
        category_service: CategoryService,
        data: CategoryCreate,
    ) -> Category:
        """Create a new Product."""
        category = data.to_dict()
        project_obj = await category_service.create(category)
        return category_service.to_schema(data=project_obj, schema_type=Category)


    @get(path=urls.CATEGORY_DETAIL)
    async def get_category(
        self,
        category_service: CategoryService,
        id: UUID = Parameter(
            title="Product ID",
            description="The Product to retrieve.",
        ),
    ) -> Category:
        """Get an existing Product."""
        obj = await category_service.get(item_id=id)
        return category_service.to_schema(data=obj,  schema_type=Category)

    @patch(
        path=urls.CATEGORY_UPDATE, guards=[requires_superuser, requires_active_user]
    )
    async def update_category(
        self,
        category_service: CategoryService,
        data: CategoryCreate,
        id: UUID = Parameter(
            title="Category ID",
            description="The Product to update.",
        ),
    ) -> Category:
        """Update an category."""
        category = data.to_dict()
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


class SubCategoryController(Controller):
    """Category CRUD"""
    tags = ["SubCategory"]
    dependencies = {"subcategory_service": Provide(provide_subcategory_service)}

    @get(path=urls.SUBCATEGORY_LIST)
    async def list_subcategory(
        self,
        subcategory_service: SubCategoryService,
        limit_offset: LimitOffset,
    ) -> OffsetPagination[SubCategory]:
        """List Products."""
        results, total = await subcategory_service.list_and_count(limit_offset)
        filters = [limit_offset]
        return subcategory_service.to_schema(data=results, total=total, schema_type=SubCategory, filters=filters)

    @post(path=urls.SUBCATEGORY_ADD, guards=[requires_superuser, requires_active_user])
    async def create_subcategory(
        self,
        subcategory_service: SubCategoryService,
        data: CategoryCreate,
    ) -> Category:
        """Create a new sub-category."""
        category = data.to_dict()
        project_obj = await subcategory_service.create(category)
        return subcategory_service.to_schema(data=project_obj, schema_type=Category)


    @get(path=urls.SUBCATEGORY_DETAIL)
    async def get_subcategory(
        self,
        subcategory_service: SubCategoryService,
        id: UUID = Parameter(
            title="Sub-category ID",
            description="The Sub-category to retrieve.",
        ),
    ) -> Category:
        """Get an existing Sub-category."""
        obj = await subcategory_service.get(item_id=id)
        return subcategory_service.to_schema(data=obj,  schema_type=Category)

    @patch(
        path=urls.SUBCATEGORY_UPDATE, guards=[requires_superuser, requires_active_user]
    )
    async def update_subcategory(
        self,
        subcategory_service: SubCategoryService,
        data: CategoryCreate,
        id: UUID = Parameter(
            title="Category ID",
            description="The sub-category to update.",
        ),
    ) -> Category:
        """Update an sub-category."""
        category = data.to_dict()
        db_obj = await subcategory_service.update(item_id=id, data=category)
        return subcategory_service.to_schema(db_obj, schema_type=Category)