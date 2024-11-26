from __future__ import annotations

import os
import typesense
from logging import getLogger
from typing import Any, TYPE_CHECKING, Type
from db.models import Product
from domain.products.schemas import TypesenseProductSchema, Product as ProductSchema
from domain.repositories import ProductRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from dotenv import load_dotenv

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
            # product_related_content_embed = product.category.context_embedding
            # product_related_content = product.category.context_embedding
            # if product_related_content is None:
            #     return [0.00] # not allow to generate embedding without related content of category 
            text = f"Product Name: {product.name}, Brand: {product.brand}, Price:${product.price}, Description: {product.description}."
            # product_info_embedding = embedding_model.encode(text).tolist()
            # return [x + y for x, y in zip(product_info_embedding, product_info_embedding)]
            return embedding_model.encode(text).tolist()
        else:
            return embedding_model.encode(query).tolist()


    async def bulk_insert_into_typesense(self, typesense_client: typesense.Client, products: list[TypesenseProductSchema]) ->list[dict[str, Any]]:
        try:
            products = [product.dict() for product in products]
            return typesense_client.collections[COLLECTION_NAME].documents.import_(products, {'action': 'upsert'})
        except typesense.exceptions.RequestMalformed as e:
            logger.error(f"Failed to insert data into Typesense: {e}")
            return [{"success":False, "error": "Failed to import in the bulk insert"}]


    async def add_product_into_typesense(self, typesense_client: typesense.Client, product: TypesenseProductSchema) -> bool:
        try:
            product = product.dict()
            res = typesense_client.collections[COLLECTION_NAME].documents.import_([product], {'action': 'upsert'})
            return res[0]['success']
        except typesense.exceptions.RequestMalformed as e:
            logger.error(f"Failed to add product into Typesense: {e}")
        return False

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


    async def get_products_for_typesense(self,  embedding_model:SentenceTransformer, products:list[Product]) -> list[TypesenseProductSchema]:
 
        # Prepare data for Typesense
        typesense_data = []
        for product in products:
            product_rating = sum(review.rating for review in product.product_reviews) / len(product.product_reviews) if product.product_reviews else 0
            embedding = await self.generate_embedding(embedding_model=embedding_model, product=product)
            
            tags = [product_tag.tag.name for product_tag in product.product_tags]
            discountPrice = float(product.price)
            price = float(product.price)
            discountPercent = float(product.discount_percent)
            if discountPercent > 0:
                discountPrice = price * (1 - discountPercent / 100)
            
            product_data = TypesenseProductSchema(
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
                tags = tags if len(tags)>0 != None else [""],
            )
            typesense_data.append(product_data)
        return typesense_data