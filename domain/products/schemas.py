from pydantic import BaseModel

class ProductCreate(BaseModel):
    name:str
    description: str
    price: float
    image_url:str
    brand:str
    category_id: int
    subcategory_id: int
    sub_image_url:dict ={}
    stock:int =0
    discount_percent:float = 0.0

