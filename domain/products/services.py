from __future__ import annotations

import typesense
from typing import Any  
from db.models import Product
from domain.repositories import ProductRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService


 
class ProductService(SQLAlchemyAsyncRepositoryService[Product]):
    """Handles database operations for products."""

    repository_type = ProductRepository

    def __init__(self, **repo_kwargs: Any) -> None:
        self.repository: ProductRepository = self.repository_type(**repo_kwargs)
        self.model_type = self.repository.model_type

    
    async def bulk_insert_into_typesense(self):
        data = await self.get_products_for_typesense()
        # Bulk insert into Typesense
        try:
            self.typesense_client.collections['products-collection'].documents.import_(data, {'action': 'upsert'})
        except typesense.exceptions.RequestMalformed as e:
            print(f"Failed to insert data into Typesense: {e}")