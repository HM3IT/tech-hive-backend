from uuid import UUID 
from domain.lib.schema import CamelizedBaseStruct


class CategoryCreate(CamelizedBaseStruct):
    name:str
 

class Category(CamelizedBaseStruct):
    id:UUID
    name:str
 
 
class SubCategory(CamelizedBaseStruct):
    id:UUID
    name:str
    category_id:UUID
 