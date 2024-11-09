from uuid import UUID 
from domain.lib.schema import CamelizedBaseStruct


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


class Product(CamelizedBaseStruct):
    id:UUID
    name:str
    description: str
    image_url:str
    brand:str
    category_id: UUID
    price: float= 0.0
    stock:int =0
    sub_image_url:dict ={}
    discount_percent:float = 0.0
