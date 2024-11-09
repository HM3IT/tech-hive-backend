from __future__ import annotations

from typing import TYPE_CHECKING

from litestar import get, post, delete, patch
from litestar.exceptions import HTTPException
from litestar.controller import Controller
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from litestar.repository.filters import LimitOffset
from domain.products.depedencies import provide_product_service
from domain.products.services import ProductService
from domain.products import urls
from domain.products.schemas import ProductCreate, Product
from domain.users.guards import requires_active_user, requires_superuser

if TYPE_CHECKING:
    from uuid import UUID

class ProductController(Controller):
    """Product CRUD"""

    dependencies = {"product_service": Provide(provide_product_service)}

    @get(path=urls.PRODUCT_LIST)
    async def list_products(
        self,
        product_service: ProductService,
        limit_offset: LimitOffset,
    ) -> OffsetPagination[Product]:
        """List Products."""
        results, total = await product_service.list_and_count(limit_offset)

        filters = [limit_offset]
 
        return product_service.to_schema(data=results, total=total, schema_type=Product, filters=filters)

    @post(path=urls.PRODUCT_ADD, guards=[requires_superuser, requires_active_user])
    async def create_product(
        self,
        product_service: ProductService,
        data: ProductCreate,
    ) -> Product:
        """Create a new Product."""
        product = data.to_dict()
        project_obj = await product_service.create(product)
        return product_service.to_schema(data=project_obj, schema_type=Product)


    @get(path=urls.PRODUCT_DETAIL)
    async def get_product(
        self,
        product_service: ProductService,
        id: UUID = Parameter(
            title="Product ID",
            description="The Product to retrieve.",
        ),
    ) -> Product:
        """Get an existing Product."""
        obj = await product_service.get(item_id=id)
        return product_service.to_schema(data=obj,  schema_type=Product)

    @patch(
        path=urls.PRODUCT_UPDATE, guards=[requires_superuser, requires_active_user]
    )
    async def update_product(
        self,
        product_service: ProductService,
        data: ProductCreate,
        id: UUID = Parameter(
            title="Product ID",
            description="The Product to update.",
        ),
    ) -> Product:
        """Update an Product."""
        product = data.to_dict()
        # item_id = product.get("id")
        # if item_id is None:
        #     raise HTTPException(detail="Product Id must included", status_code = 400)
        db_obj = await product_service.update(item_id=id, data=product)
        return product_service.to_schema(db_obj, schema_type=Product)

    @delete(path=urls.PRODUCT_REMOVE, guards=[requires_superuser, requires_active_user])
    async def delete_product(
        self,
        product_service: ProductService,
        id: UUID = Parameter(
            title="Product ID",
            description="The Product to delete.",
        ),
    ) -> None:
        """Delete a Product from the system."""
        await product_service.delete(item_id=id)

