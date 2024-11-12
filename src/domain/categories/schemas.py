from uuid import UUID 
from domain.lib.schema import CamelizedBaseStruct



 
class SubCategoryCreate(CamelizedBaseStruct):
    category_id:UUID
    name:str
 

class SubCategory(CamelizedBaseStruct):
    id:UUID
    name:str
 
class CategoryUpdate(CamelizedBaseStruct):
    name:str
 

class CategoryCreate(CamelizedBaseStruct):
    name:str
    SubCategories:list[str] = []
 

class Category(CamelizedBaseStruct):
    id:UUID
    name:str
    sub_categories: list[dict[str, str]] = []
 