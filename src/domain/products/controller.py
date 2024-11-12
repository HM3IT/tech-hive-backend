from __future__ import annotations

import os

from typing import Annotated
from litestar.params import Body
from litestar.datastructures import UploadFile
from litestar import get, post, delete, patch, Response
from litestar.enums import RequestEncodingType
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
from dotenv import load_dotenv 
from uuid import uuid4, UUID

load_dotenv()

IMG_FILE_PATH = os.environ["IMG_FILE_PATH"]
ACCEPTED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg",]

class ProductController(Controller):
    """Product CRUD"""
    tags = ["Product"]
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

    @post(path=urls.PRODUCT_IMG_UPLOAD, guards=[requires_superuser, requires_active_user])
    async def upload_img_file(
        self,
        product_service: ProductService,
        data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
    ) -> Response:
        """Create a new Product."""
        filename = data.filename
        file_type = data.content_type

        if file_type not in ACCEPTED_IMAGE_TYPES:
             raise HTTPException(status_code=400, detail="Unsupported file type. Only JPEG, PNG, and JPG are allowed.")
        content = await data.read()
        file_UUID = uuid4()
        file_path = f"{IMG_FILE_PATH}/{file_UUID}_{filename}"
        with open(file_path, mode="wb") as f:
            f.write(content)
 
        return Response(content={"file_path":file_path}, status_code=201)


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

