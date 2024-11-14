from __future__ import annotations

import os
from logging import getLogger
# import typesense
from typing import Any  
from db.models import Product
from domain.products.schemas import TypesenseProductSchema
from domain.repositories import ProductRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
# from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

COLLECTION_NAME = os.environ["TYPESENSE_PRODUCT_COLLECTION_NAME"]
EMBEDDING_MODEL = os.environ["EMBEDDING_MODEL"]

logger = getLogger()

class ProductService(SQLAlchemyAsyncRepositoryService[Product]):
    """Handles database operations for products."""

    repository_type = ProductRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: ProductRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type
        # self.embedding_model = SentenceTransformer(EMBEDDING_MODEL) 

    # async def generate_embedding(self, product: Product) -> list[float]:
    #     text = f"Product Name: {product.name}, Price:{product.price}, Description: {product.description}"
    #     return self.embedding_model.encode(text).tolist()

    # async def bulk_insert_into_typesense(self, typesense_client: typesense.Client, products: list[TypesenseProductSchema]):
    #     try:
    #         typesense_client.collections[COLLECTION_NAME].documents.import_(products, {'action': 'upsert'})
    #     except typesense.exceptions.RequestMalformed as e:
    #         logger.error(f"Failed to insert data into Typesense: {e}")


    # async def add_product_into_typesense(self, typesense_client: typesense.Client, product: dict[str, Any]) -> bool:
    #     try:
    #         TypesenseProductSchema(**product)
    #         typesense_client.collections[COLLECTION_NAME].documents.import_([product], {'action': 'upsert'})
    #         return True
    #     except typesense.exceptions.RequestMalformed as e:
    #         logger.error(f"Failed to add product into Typesense: {e}")
    #     return False

    # async def get_products_for_typesense(self, products:list[Product]) -> list[dict]:
 
    #     # Prepare data for Typesense
    #     typesense_data = []
    #     for product in products:
    #         product_rating = sum(review.rating for review in product.product_reviews) / len(product.product_reviews) if product.product_reviews else 0
    #         typesense_data.append({
    #             "id": str(product.id),
    #             "name": product.name,
    #             "description": product.description,
    #             "price": float(product.price),
    #             "discount_percent": float(product.discount_percent),
    #             "brand": product.brand,
    #             "stock": product.stock,
    #             "sold": product.sold,
    #             "category_name": product.category_name,
    #             "product_rating": product_rating,

    #             "embedding": self.generate_embedding(product) 
    #         })
    #     return typesense_data