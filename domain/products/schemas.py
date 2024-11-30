from uuid import UUID 
from domain.lib.schema import CamelizedBaseStruct
from pydantic import BaseModel
from datetime import datetime

class ProductCreate(CamelizedBaseStruct):
    name:str
    description: str
    price: float
    image_url:str
    brand:str
    category_id: UUID
    sub_image_url:dict ={}
    stock:int =0
    discount_percent:float = 0.0


class ProductUpdate(CamelizedBaseStruct):
    name:str
    description: str
    price: float
    image_url:str
    brand:str
    category_id: UUID
    sub_image_url:dict ={}
    stock:int =0
    tag_ids:list[str] | None = None
    discount_percent:float = 0.0


class Category(CamelizedBaseStruct):
    id: UUID
    name: str
    related_context:str

class Product(CamelizedBaseStruct):
    id:UUID
    name:str
    description: str
    image_url:str
    brand:str
    category_id: UUID
    category:Category
    price: float= 0.0
    stock:int =0
    sub_image_url:dict ={}
    discount_percent:float = 0.0

class ProductTag(CamelizedBaseStruct):
    id: UUID
    product_id: UUID
    tag_id: UUID

class ProductDetail(CamelizedBaseStruct):
    id:UUID
    name:str
    description: str
    image_url:str
    brand:str
    overall_rating:float
    category_id: UUID
    price: float= 0.0
    stock:int =0
    sub_image_url:dict ={}
    product_tags:list[ProductTag] |None = None
    discount_percent:float = 0.0

 
class TypesenseProductSchema(BaseModel):
    id: str
    name: str
    description:str
    price: float
    discountPercent: float
    discountPrice:float
    brand: str
    stock: int
    sold: int
    categoryName: str 
    imageUrl:str 
    embedding: list[float]
    productRating: float = 0.0 
    tags:list[str] = [""]


class SemanticSearch(BaseModel):
    query: str
 

class ProductReview(CamelizedBaseStruct):
    user_id: UUID
    product_id: UUID
    rating: float
    review_text: str
    created_at: datetime
    updated_at:datetime


class ProductReviewCreate(CamelizedBaseStruct):
    product_id: UUID
    rating: float
    review_text: str
   