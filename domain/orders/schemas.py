from __future__ import annotations

from domain.lib.schema import CamelizedBaseStruct
 
from uuid import UUID

from db.models import OrderStatus
from domain.products.schemas import Product
from datetime import datetime

__all__ = (
    "Order",
    "OrderCreate",
    "OrderUpdate",
    "OrderProduct",
)


class Order(CamelizedBaseStruct):
    id:UUID
    user_id: UUID
    address:str
    total_price: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

class OrderDetail(CamelizedBaseStruct):
    id:UUID
    user_id: UUID
    address:str
    total_price: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    order_products:list[OrderProduct]

class OrderProductCreate(CamelizedBaseStruct):
    order_id:UUID
    product_id:UUID
    quantity: int
    price_at_order:float
    discount_percent_at_order:float
    
class CartProduct(CamelizedBaseStruct):
    product_id:UUID
    price_at_order:float
    discount_percent_at_order:float
    quantity:int

class OrderCreate(CamelizedBaseStruct):
    order_products: list[CartProduct]
    address:str
    total_price: float
    

class OrderUpdate(CamelizedBaseStruct):
    id:UUID
    order_status:OrderStatus

class OrderProduct(CamelizedBaseStruct):
    product_id:UUID
    quantity: int
    price_at_order:float
    discount_percent_at_order:float
 


