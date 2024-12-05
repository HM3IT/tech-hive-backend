from __future__ import annotations

import os
import typesense
from logging import getLogger
from dotenv import load_dotenv
from typing import Any, TYPE_CHECKING

from litestar.exceptions import HTTPException

from db.models import Product, ProductReview
from domain.products.schemas import TypesenseProductSchema
from domain.repositories import ProductRepository, ProductReviewRepository

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer


load_dotenv()

COLLECTION_NAME = os.environ["TYPESENSE_PRODUCT_COLLECTION_NAME"]

logger = getLogger()

class ProductService(SQLAlchemyAsyncRepositoryService[Product]):
    """Handles database operations for products."""

    repository_type = ProductRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: ProductRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    async def generate_embedding(self, embedding_model:SentenceTransformer, product: Product|None = None, query:str="") -> list[float]:
        if product:
            text = f"Product Name: {product.name}, Brand: {product.brand}, Price:${product.price}, Description: {product.description}."
            return embedding_model.encode(text).tolist()
        # if product:
        #     product_related_content_embed = product.category.context_embedding
        #     product_related_content = product.category.context_embedding
        #     if product_related_content is None:
        #         return [0.00] # not allow to generate embedding without related content of category 
        #     text = f"Product Name: {product.name}, Brand: {product.brand}, Price:${product.price}, Description: {product.description}."
        #     product_info_embedding = embedding_model.encode(text).tolist()
        #     return [x + y for x, y in zip(product_info_embedding, product_info_embedding)]
        #     return embedding_model.encode(text).tolist()
        # else:
        #     return embedding_model.encode(query).tolist()


    async def bulk_insert_into_typesense(self, typesense_client: typesense.Client, products: list[TypesenseProductSchema]) ->list[dict[str, Any]]:
        try:
            products = [product.dict() for product in products]
            return typesense_client.collections[COLLECTION_NAME].documents.import_(products, {'action': 'upsert'})
        except typesense.exceptions.RequestMalformed as e:
            logger.error(f"Failed to insert data into Typesense: {e}")
            return [{"success":False, "error": "Failed to import in the bulk insert"}]


    async def delete_product_from_typesense(self, typesense_client: typesense.Client, document_id: str) -> bool:
        try:
            typesense_client.collections[COLLECTION_NAME].documents[document_id].delete()
            logger.info(f"Successfully deleted document with ID: {document_id}")
            return True
        except typesense.exceptions.ObjectNotFound as e:
            logger.warning(f"Document with ID {document_id} not found: {e}")
        except typesense.exceptions.TypesenseClientError as e:
            logger.error(f"Error occurred while deleting document with ID {document_id}: {e}")
        return False

    async def convert_typesense_product(self, product:Product, embedding:list[float]) ->TypesenseProductSchema:
        product_rating = sum(review.rating for review in product.product_reviews) / len(product.product_reviews) if product.product_reviews else 0
        tags = [product_tag.tag.name for product_tag in product.product_tags]
        discountPrice = float(product.price)
        price = float(product.price)
        discountPercent = float(product.discount_percent)
        if discountPercent > 0:
            discountPrice = price * (1 - discountPercent / 100)
        return TypesenseProductSchema(
            id=str(product.id),
            name=product.name,
            description=product.description,
            price=price,
            discountPercent=discountPercent,
            discountPrice = discountPrice,
            brand=product.brand,
            stock=product.stock,
            sold=product.sold if product.sold is not None else 0,
            categoryName=product.category.name,
            productRating=product_rating,
            embedding=embedding,
            imageUrl = product.image_url,
            tags = tags if len(tags) > 0 != None else [""],
        )

    async def update_products_typesense(self, typesense_client: typesense.Client, product:Product) -> bool:
        try:
            embedding = await self.get_old_embedding(typesense_client, str(product.id))

            update_typesense_product = await self.convert_typesense_product(product, embedding)
  
            typesense_client.collections[COLLECTION_NAME].documents[str(product.id)].delete()
            documents_status = typesense_client.collections[COLLECTION_NAME].documents.import_([update_typesense_product.dict()], {'action': 'upsert'})
            logger.error("Updated status")
            logger.error(documents_status)
            failed_documents = [
                doc.get("error", "Unknown error") for doc in documents_status if not doc.get("success", False)
            ]
            if failed_documents:
                raise HTTPException(detail=f"Failed to update {str(product.id)}'s embedding")
            return True

        except Exception as err:
            logger.error(f"Failed to update typesense {err}")
            raise HTTPException(detail=f"Failed to update {str(product.id)}'s embedding")
 
    async def add_new_products_typesense(self, typesense_client: typesense.Client, products:list[Product]) -> bool:
        from sentence_transformers import SentenceTransformer # loading sentence transformer inside for optimization
        
        EMBEDDING_MODEL = os.environ["EMBEDDING_MODEL"]
        embedding_model = SentenceTransformer(EMBEDDING_MODEL) 
 
        # Prepare data for Typesense
        typesense_data:list[TypesenseProductSchema] = []
        for product in products:
      
            embedding = await self.generate_embedding(embedding_model=embedding_model, product=product)
 
            product_data =await self.convert_typesense_product(product, embedding)
            typesense_data.append(product_data)

        document_statuses = await self.bulk_insert_into_typesense(typesense_client, typesense_data)
        failed_documents = [
            doc.get("error", "Unknown error") for doc in document_statuses if not doc.get("success", False)
        ]
        if failed_documents:
            raise HTTPException(detail=f"Failed to update {str(product.id)}'s embedding")
        return True
       

    async def get_old_embedding(self, typesense_client: typesense.Client, document_id)-> list[float]:
        try:
            
            old_document = typesense_client.collections[COLLECTION_NAME].documents[document_id].retrieve()
            return old_document["embedding"]
            
        except Exception as e:
            logger.error(f"Error failed to retrieved embedding: {e}")
    
            raise HTTPException(detail=f"Failed to retrieve {document_id}'s embedding")
            
 
class ProductReviewService(SQLAlchemyAsyncRepositoryService[ProductReview]):

    repository_type = ProductReviewRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: ProductReviewRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type