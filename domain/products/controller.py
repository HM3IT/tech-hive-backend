from __future__ import annotations

import os
import tempfile
import mimetypes
import typesense
from decimal import Decimal, getcontext
from typing import Annotated
from litestar.params import Body
from litestar.datastructures import UploadFile
from litestar import get, post, delete, patch, Response, Request
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
from domain.products.schemas import ProductCreate, Product, SemanticSearch
from domain.users.guards import requires_active_user, requires_superuser
from dotenv import load_dotenv 
from uuid import uuid4, UUID
from litestar.response import File
from logging import getLogger
from urllib.parse import unquote

load_dotenv()

IMG_FILE_PATH = os.environ["IMG_FILE_PATH"]
ACCEPTED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg",]


DISTANCE_THRESHOLD = os.environ.get("DISTANCE_THRESHOLD", 0.43)
EMBEDDING_MODEL = os.environ["EMBEDDING_MODEL"]
TYPESENSE_HOST = os.environ["TYPESENSE_HOST"]
TYPESENSE_PORT = os.environ["TYPESENSE_PORT"]
TYPESENSE_PROTOCOL = os.environ["TYPESENSE_PROTOCOL"]
TYPESENSE_API_KEY = os.environ["TYPESENSE_API_KEY"]

logger = getLogger()
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
        # typesense_product = await product_service.get_products_for_typesense(embedding_model, [project_obj])
 
        # isSuccess = await product_service.add_product_into_typesense(typesense_client=typesense_client, product=typesense_product[0])
        # if not isSuccess:
        #     raise HTTPException(detail="Failed to add product to typesene", status_code=500)
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

    @get(path=urls.GET_IMG)
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

    #  ======================
    # Typesense part
    #  ======================

    @post(path=urls.PRODUCT_SYNC_TYPESNSE, guards=[requires_superuser])
    async def sync_products_to_typesense(self, product_service: ProductService) -> Response:
        from sentence_transformers import SentenceTransformer # loading sentence transformer inside for optimization

        embedding_model = SentenceTransformer(EMBEDDING_MODEL) 
        limit_offset = LimitOffset(limit=250, offset=0)
        results, total = await product_service.list_and_count(limit_offset)
     
        typesense_products = await product_service.get_products_for_typesense(embedding_model=embedding_model, products = list(results))
        documents_status = await product_service.bulk_insert_into_typesense(typesense_client=typesense_client, products=typesense_products)
        
        failed_documents = [
            doc.get("error", "Unknown error") for doc in documents_status if not doc.get("success", False)
        ]

        if failed_documents:
            return Response(
                content={
                    "status": "Failure",
                    "message": "Some products failed to sync to Typesense",
                    "errors": failed_documents
                },
                status_code=500
            )
        else:
            return Response(
                content={"status": "Success", "message": "All products synced to Typesense"},
                status_code=201
            )
    # Temporarily permit for admin/super users only 
    @post(path=urls.PRODUCT_SEMANTIC_SEARCH, guards=[requires_superuser])
    async def semantic_search_products(self,product_service: ProductService, data: SemanticSearch = Parameter(
            title="the query to search product semantically",
            description="The Product description or characterisitc to search with natural lagunage leveraging the power of AI.",
        ),) -> list[dict]:
        from sentence_transformers import SentenceTransformer # loading sentence transformer inside for optimization
        
        DISTANCE_THRESHOLD = os.environ["DISTANCE_THRESHOLD"]
        EMBEDDING_MODEL = os.environ["EMBEDDING_MODEL"]
        embedding_model = SentenceTransformer(EMBEDDING_MODEL) 
 
        query_embedding = await product_service.generate_embedding(embedding_model=embedding_model, query=data.query)
   
        search_requests = {
            'searches': [
                {
                    'collection': 'products-collection', 
                    'q': data.query,  
                    'vector_query': f"embedding:({query_embedding}, k:10)",  
                    'include_fields': 'id, name', 
                    'limit': 10 
                }
            ]
        }

        common_search_params =  {
            'query_by': 'embedding',
        }
 
        search_results = typesense_client.multi_search.perform(search_requests, common_search_params)
        hits = search_results['results'][0]['hits'] 
        logger.info(hits)
    
        getcontext().prec = 20  
        
        DISTANCE_THRESHOLD = Decimal(float(DISTANCE_THRESHOLD)) + Decimal(0.00001)
        filtered_hits = [
            hit for hit in hits if Decimal(str(float(hit.get('vector_distance', float('inf'))))) <= DISTANCE_THRESHOLD
        ]

        filtered_hits.sort(key=lambda x: float(x['vector_distance']))

        return filtered_hits
  
    @get(path=urls.PRODUCT_ADVANCED_SEARCH, guards=[requires_superuser])
    async def search_products(self, 
        name:str|None = None,
        category: str|None = None, 
        tags: str|None = None,
        page: int = 1,
        limit: int = 10,
        brand: str|None = None,
        price_range: str|None = None
    )-> Response:
        try:
            filters = []
            if name:
                filters.append(f"name: {name}")

            if price_range:
                min_price, max_price = price_range.split(":")
                filters.append(f"price:>{min_price} && price:<{max_price}")

            if category:
                filters.append(f"category_name:={category}")
 
            if brand:
                filters.append(f"brand:={brand}")
 
            if tags:
                filters.append(f"tags:=[{tags}]")
 
            filter_by = " && ".join(filters) if filters else ""
            logger.info("Filter by")
            logger.info(filter_by)
            search_param = {
                "q": "*",  
                "query_by": "name, description, brand, category_name", 
                "filter_by": filter_by,  
                "sort_by": "product_rating:desc",  
                "page": page,
                "per_page": limit,
                "exclude_fields": "embedding"  
            }
 
            response = typesense_client.collections[
                os.environ["TYPESENSE_PRODUCT_COLLECTION_NAME"]
            ].documents.search(search_param)

     
            return Response(
                status_code=200,
                content={
                    "Items": response.get("hits"),
                    "Total": response.get("found"),
                    "Page": response.get("page"),
                    "Per_Page": response.get("per_page")
                },
            )
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response(status_code=500, content={"error": f"Internal Server Error: {e}"})