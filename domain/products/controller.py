from __future__ import annotations

import os
import tempfile
import mimetypes
import typesense
from decimal import Decimal, getcontext
from typing import Annotated
from litestar.params import Body
from litestar.datastructures import UploadFile
from litestar import get, post, delete, patch, Response, Request, MediaType
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.controller import Controller
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from litestar.repository.filters import LimitOffset

from uuid import UUID
from domain.products.depedencies import provide_product_service

from domain.tags.depedencies import provide_tag_service, provide_product_tag_service
from domain.tags.services import TagService, ProductTagService

from domain.products.services import ProductService
from domain.products import urls
from domain.products.schemas import ProductCreate, ProductUpdate, Product, ProductDetail, SemanticSearch
from domain.tags.schemas import ProductTagCreate, ProductTag
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
    dependencies = {
        "product_service": Provide(provide_product_service),
        "tag_service": Provide(provide_tag_service),
        "product_tag_service": Provide(provide_product_tag_service)
    }

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
        # from sentence_transformers import SentenceTransformer # loading sentence transformer inside for optimization
        
        # EMBEDDING_MODEL = os.environ["EMBEDDING_MODEL"]
        # embedding_model = SentenceTransformer(EMBEDDING_MODEL) 
   
        """Create a new Product."""
        product = data.to_dict()
        product.update({"sold":0})
        project_obj = await product_service.create(product)
        # try:
        #     # Typesense synchronization upon product creation
        #     typesense_product = await product_service.get_products_for_typesense(embedding_model, [project_obj])
        #     await product_service.add_product_into_typesense(typesense_client=typesense_client, product=typesense_product[0])
            
        # except Exception as e:
        #     logger.error(f"Sync failed at product creation, Error: {e}")
        return product_service.to_schema(data=project_obj, schema_type=Product)

    @post(path=urls.PRODUCT_IMG_UPLOAD, guards=[requires_active_user])
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
        product_tag_service:ProductTagService,
        id: UUID = Parameter(
            title="Product ID",
            description="The Product to retrieve.",
        ),
    ) -> ProductDetail:
        """Get an existing Product."""
        db_obj = await product_service.get(item_id=id)
        product_tags = []
        if db_obj.product_tags:
            product_tag_res = product_tag_service.to_schema(data=db_obj.product_tags, total=len(db_obj.product_tags), schema_type=ProductTag)
            product_tags = product_tag_res.items

        return ProductDetail(
            id = db_obj.id,
            name = db_obj.name,
            description = db_obj.description,
            image_url = db_obj.image_url,
            brand = db_obj.brand,
            category_id =db_obj.category_id,
            price = db_obj.price,
            stock = db_obj.stock,
            sub_image_url = db_obj.sub_image_url,
            product_tags = product_tags,
            discount_percent = db_obj.discount_percent
        )

    @patch(
        path=urls.PRODUCT_UPDATE, guards=[requires_superuser, requires_active_user]
    )
    async def update_product(
        self,
        product_service: ProductService,
        tag_service: TagService,
        product_tag_service:ProductTagService,
        data: ProductUpdate,
        id: UUID = Parameter(
            title="Product ID",
            description="The Product to be updated.",
        ),
    ) -> bool:
        """Update an Product."""
        # from sentence_transformers import SentenceTransformer # loading sentence transformer inside for optimization
        
        # EMBEDDING_MODEL = os.environ["EMBEDDING_MODEL"]
        # embedding_model = SentenceTransformer(EMBEDDING_MODEL) 
        product = data.to_dict()
        db_obj = await product_service.get(item_id=id)
        if not db_obj:
            raise HTTPException(detail="Product Id not found", status_code= 404 )
        update_tag_ids = product.pop("tag_ids")
        db_obj = await product_service.update(item_id=str(id), data=product)
   
        existing_tag_ids = {tag.tag_id for tag in db_obj.product_tags}
        
        if len(update_tag_ids) <= 0:
            return True

        for tag_id in update_tag_ids:
            tag_obj = await tag_service.get_one_or_none(id=tag_id)
            if not tag_obj:
                raise HTTPException(detail="Tag Id not found", status_code= 404 )

        new_tag_ids = set(update_tag_ids) - existing_tag_ids
     
        product_tag_objs = []  
        for tag_id in new_tag_ids:
       
            product_tag_obj = await product_tag_service.create(data={"product_id": str(id), "tag_id": tag_id})

            product_tag_objs.append(product_tag_obj)

        old_tag_ids = existing_tag_ids - set(update_tag_ids)

        for deleted_tag_id in old_tag_ids:  
            logger.info("Deleting tag with ID: %s", deleted_tag_id)
            
            for product_tag in db_obj.product_tags:
                if product_tag.tag_id == deleted_tag_id:
                    await product_tag_service.delete(item_id=product_tag.id)
 
        # try:
        #     isSuccess = await product_service.delete_product_from_typesense(typesense_client=typesense_client, document_id=str(id))
        #     if isSuccess:
        #         product_typesense = await product_service.get_products_for_typesense(embedding_model, [product])
        #         await product_service.add_product_into_typesense(typesense_client=typesense_client, product=product_typesense[0])
        # except Exception as e:
        #     logger.error(f"Update product sync failed: {e}")

        return True


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


    @post(path=urls.PRODUCT_EMBEDDING, guards=[requires_superuser])
    async def generate_embedding_product(
        self,
        product_service: ProductService,
        id:UUID = Parameter(
            title="Product ID",
            description="The Product to delete.",
        )
    ) -> Response:
        """Create a new Product."""
        from sentence_transformers import SentenceTransformer # loading sentence transformer inside for optimization
        
        EMBEDDING_MODEL = os.environ["EMBEDDING_MODEL"]
        embedding_model = SentenceTransformer(EMBEDDING_MODEL) 
        db_obj = await product_service.get(item_id=id)
        if not db_obj:
            raise HTTPException(detail="Product has not created", status_code=404)

        typesense_products = await product_service.get_products_for_typesense(embedding_model=embedding_model, products = [db_obj])
     
        documents_status = await product_service.bulk_insert_into_typesense(typesense_client=typesense_client, products=typesense_products)
        
        failed_documents = [
            doc.get("error", "Unknown error") for doc in documents_status if not doc.get("success", False)
        ]

        if failed_documents:
            return Response(
                content={
                    "status": "Failure",
                    "message": "Product failed to sync Typesense",
                    "errors": failed_documents
                },
                status_code=500
            )
        else:
            return Response(
                content={"status": "Success", "message": f"Product {db_obj.id}  has synced to Typesense"},
                status_code=201
            )


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
         
        isSuccess = await product_service.delete_product_from_typesense(typesense_client=typesense_client, document_id=str(id))
        if not isSuccess:
            logger.error(f"Failed to delete document {id} from Typesense")
    
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
                    'q': "*",  
                    'vector_query': f"embedding:({query_embedding}, k:10)",  
                    'include_fields': 'id, name', 
                    'limit': 30 
                }
            ]
        }

        common_search_params =  {
            'query_by': 'embedding',
        }
 
        search_results = typesense_client.multi_search.perform(search_requests, common_search_params)
  
        hits = search_results['results'][0]['hits'] 
        logger.info(hits)
        if len(hits) <= 0:
            return []
    
        getcontext().prec = 20  
        
        DISTANCE_THRESHOLD = Decimal(float(DISTANCE_THRESHOLD)) + Decimal(0.00001)
        filtered_hits = [
            hit for hit in hits if Decimal(str(float(hit.get('vector_distance', float('inf'))))) <= DISTANCE_THRESHOLD
        ]

        filtered_hits.sort(key=lambda x: float(x['vector_distance']))

        return filtered_hits
  
    @get(path=urls.PRODUCT_ADVANCED_SEARCH)
    async def search_products(self, 
        query_str: str|None,
        page: int = 1,
        limit: int = 10,
        price_range: str | None = None
    ) -> Response:
        try:
         
            filters = ""
            if price_range and price_range != "null":
                min_price, max_price = price_range.split(":")
                if not min_price:
                    filters =  f"discountPrice:=>{max_price}"
                else:
                    filters =  f"discountPrice:[{min_price}..{max_price}]"
            if query_str in ("None","null"):
                query_str = "*"

            search_param = {
                "q": query_str,  
                "query_by": "name, brand, categoryName", 
                "filter_by": filters, 
                "sort_by": "productRating:desc, sold:desc",  
                "page": page,
                "per_page": limit,
                "exclude_fields": "embedding"  
            }

            response = typesense_client.collections[
                os.environ["TYPESENSE_PRODUCT_COLLECTION_NAME"]
            ].documents.search(search_param)

            logger.info(response)
            return Response(
                status_code=200,
                content={
                    "items": response.get("hits"),
                    "total": response.get("found"),
                    "page": response.get("page"),
                    "per_page": limit
                },
            )
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response(status_code=500, content={"error": f"Internal Server Error: {e}"})