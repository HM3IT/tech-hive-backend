from __future__ import annotations

import os
import typesense
from logging import getLogger
from typing import Any, TYPE_CHECKING
from db.models import Product
from domain.products.schemas import TypesenseProductSchema
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
        text = query
        if product:
            text = f"Product Name: {product.name}, Price:{product.price}, Description: {product.description}"
        
        return embedding_model.encode(text).tolist()

    async def bulk_insert_into_typesense(self, typesense_client: typesense.Client, products: list[TypesenseProductSchema]) ->list[dict[str, Any]]:
        try:
            products = [product.dict() for product in products]
            return typesense_client.collections[COLLECTION_NAME].documents.import_(products, {'action': 'upsert'})
        except typesense.exceptions.RequestMalformed as e:
            logger.error(f"Failed to insert data into Typesense: {e}")
            return [{"success":False, "error": "Failed to import in the bulk insert"}]


    async def add_product_into_typesense(self, typesense_client: typesense.Client, product: dict[str, Any]) -> bool:
        try:
            TypesenseProductSchema(**product)
            res = typesense_client.collections[COLLECTION_NAME].documents.import_([product], {'action': 'upsert'})
            return res[0]['success']
        except typesense.exceptions.RequestMalformed as e:
            logger.error(f"Failed to add product into Typesense: {e}")
        return False

    async def get_products_for_typesense(self,  embedding_model:SentenceTransformer, products:list[Product]) -> list[TypesenseProductSchema]:
 
        # Prepare data for Typesense
        typesense_data = []
        for product in products:
            product_rating = sum(review.rating for review in product.product_reviews) / len(product.product_reviews) if product.product_reviews else 0
            embedding = await self.generate_embedding(embedding_model=embedding_model, product=product)
         
            product_data = TypesenseProductSchema(
                id=str(product.id),
                name=product.name,
                description=product.description,
                price=float(product.price),
                discount_percent=float(product.discount_percent),
                brand=product.brand,
                stock=product.stock,
                sold=product.sold if product.sold is not None else 0,
                category_name=product.category.name,
                product_rating=product_rating,
                embedding=embedding
            )
            typesense_data.append(product_data)
        return typesense_data