from __future__ import annotations

import os
import tempfile
import mimetypes
import typesense
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
from domain.products.schemas import ProductCreate, Product, imageFilePath
from domain.users.guards import requires_active_user, requires_superuser
from dotenv import load_dotenv 
from uuid import uuid4, UUID
from litestar.response import File
from logging import getLogger
from urllib.parse import unquote
from logging import getLogger


logger = getLogger()
load_dotenv()

IMG_FILE_PATH = os.environ["IMG_FILE_PATH"]
ACCEPTED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg",]

TYPESENSE_HOST = os.environ["TYPESENSE_HOST"]
TYPESENSE_PORT = os.environ["TYPESENSE_PORT"]
TYPESENSE_PROTOCOL = os.environ["TYPESENSE_PROTOCOL"]
TYPESENSE_API_KEY = os.environ["TYPESENSE_API_KEY"]

typesense_client = typesense.Client({
    "nodes": [{
        "host": TYPESENSE_HOST,
        "port": TYPESENSE_PORT,
        "protocol": TYPESENSE_PROTOCOL
    }],
    "api_key": TYPESENSE_API_KEY,
    "connection_timeout_seconds": 180
})


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
        product.update({"sold":0})
        project_obj = await product_service.create(product)
        typesense_product = await product_service.get_products_for_typesense([project_obj])
        logger.error("typesense_product")
        logger.error(typesense_product)
        isSuccess = await product_service.add_product_into_typesense(typesense_client=typesense_client, product=typesense_product[0])
        if not isSuccess:
            raise HTTPException(detail="Failed to add product to typesene", status_code=500)
        return product_service.to_schema(data=project_obj, schema_type=Product)

    @post(path=urls.PRODUCT_IMG_UPLOAD)
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

    @get(path="/api/products/images/{image_name:str}")
    async def get_image(self, image_name:str ) -> File| None:
        image_name = unquote(image_name.strip())
        logger.info(f"image name {image_name}")
        image_name= image_name.strip()
        image_path = f"images/{image_name}"
        logger.info(f'Image file path {image_path}')
        if os.path.exists(f"./{image_path}"):
          
            try:
                with open(image_path, "rb") as f:
                    content: bytes = f.read()
                mime_type, _ = mimetypes.guess_type(image_path)
                extension = image_path.split(".")[-1]
         
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{extension}") as tmp_file:
                    tmp_file.write(content)
                    tmp_file.flush()
                    return File(
                        content_disposition_type="attachment",
                        path=tmp_file.name,
                        media_type=mime_type,
                    )

            except Exception as e:
                raise HTTPException(f"Failed to read document: {e!s}", status_code=500)
        return None
    

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
    ) -> Product:
        """Update an Product."""
        product = data.to_dict()
        item_id = product.pop("id")
        if item_id is None:
            raise HTTPException(detail="Product Id must included", status_code = 400)
        db_obj = await product_service.update(item_id=item_id, data=product)
        return product_service.to_schema(db_obj, schema_type=Product)


    @patch(
        path=urls.PRODUCT_IMG_UPDATE, 
        guards=[requires_superuser, requires_active_user]
    )
    async def update_product_image(
        self,
        product_service: ProductService,
        imageUrl: str = Parameter(
            title="Image URL",
            description="The new image URL for the product.",
        ),
        id: UUID = Parameter(
            title="Product ID",
            description="The ID of the product to update.",
        ),
    ) -> Product:
        """Update only the imageUrl field of a Product."""
        

        existing_product = await product_service.get_one_or_none(id=str(id))
        if not existing_product:
            raise HTTPException(detail="Product not found", status_code=404)
 
        update_data = {"image_url": imageUrl}
        
        db_obj = await product_service.update(item_id=id, data=update_data)
  
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


    # Typesense part

    @post(path="/sync-products-to-typesense")
    async def sync_products_to_typesense(self, product_service: ProductService) -> Response:
        await product_service.bulk_insert_into_typesense()
        return Response(content={"status": "Success", "message": "Products synced to Typesense"}, status_code=201)