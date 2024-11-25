from uuid import UUID 
from domain.lib.schema import CamelizedBaseStruct

 
class TagCreate(CamelizedBaseStruct):
    name:str
    description:str

class Tag(CamelizedBaseStruct):
    id:UUID
    name:str
    description:str
 
class CategoryUpdate(CamelizedBaseStruct):
    name:str
    related_context:str | None = None
    context_embedding: list[float]|None = None
 

class CategoryCreate(CamelizedBaseStruct):
    name:str
    related_context:str
 

class Category(CamelizedBaseStruct):
    id:UUID
    name:str
    related_context:str|None = None
    context_embedding: list[float]|None = None
 