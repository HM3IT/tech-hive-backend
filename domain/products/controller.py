from __future__ import annotations

from typing import TYPE_CHECKING

from litestar import get, post, update, delete

from litestar.controller import Controller
from litestar.di import Provide
from litestar.handlers.http_handlers.decorators import delete, patch, post
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from litestar.repository.filters import LimitOffset
from services import provide_product_service
from domain.repositories import ProductRepository
from domain.products.urls import PRODUCT_ADD, PRODUCT_LIST, PRODUCT_REMOVE, PRODUCT_UPDATE
from domain.products.schemas import ProductCreate
from db.models import Product as ProductModel

if TYPE_CHECKING:
    from uuid import UUID

class ProductController(Controller):
    """Product CRUD"""

    dependencies = {"product_service": Provide(provide_product_service)}

    @get(path=PRODUCT_LIST)
    async def list_products(
        self,
        product_service: ProductRepository,
        limit_offset: LimitOffset,
    ) -> OffsetPagination[ProductModel]:
        """List Products."""
        results, total = await product_service.list_and_count(limit_offset)
     
        return OffsetPagination[ProductModel](
            items=results,
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @post(path=PRODUCT_ADD)
    async def create_Product(
        self,
        product_service: ProductRepository,
        data: ProductCreate,
    ) -> ProductModel:
        """Create a new Product."""
        obj = await product_service.add(
            ProductModel(**data.model_dump(exclude_unset=True, exclude_none=True)),
        )
        return ProductModel.model_validate(obj)


    @get(path="/Products/{id:uuid}")
    async def get_Product(
        self,
        product_service: ProductRepository,
        id: UUID = Parameter(
            title="Product ID",
            description="The Product to retrieve.",
        ),
    ) -> ProductModel:
        """Get an existing Product."""
        obj = await product_service.get(id)
        return ProductModel.model_validate(obj)

    @patch(
        path="/Products/{Product_id:uuid}"
    )
    async def update_Product(
        self,
        product_service: ProductRepository,
        data: ProductCreate,
        Product_id: UUID = Parameter(
            title="Product ID",
            description="The Product to update.",
        ),
    ) -> ProductModel:
        """Update an Product."""
        raw_obj = data.model_dump(exclude_unset=True, exclude_none=True)
        raw_obj.update({"id": Product_id})
        obj = await product_service.update(ProductModel(**raw_obj))
        return ProductModel.from_orm(obj)

    @delete(path="/Products/{Product_id:uuid}")
    async def delete_Product(
        self,
        product_service: ProductRepository,
        Product_id: UUID = Parameter(
            title="Product ID",
            description="The Product to delete.",
        ),
    ) -> None:
        """Delete a Product from the system."""
        await product_service.delete(Product_id)

