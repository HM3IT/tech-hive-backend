from uuid import UUID 
from domain.lib.schema import CamelizedBaseStruct
from pydantic import BaseModel
from pydantic import BaseModel
from pydantic import field_validator
from litestar.datastructures import UploadFile

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

class Category(CamelizedBaseStruct):
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


class SemanticSearch(BaseModel):
    query: str
 