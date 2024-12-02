from __future__ import annotations

from domain.lib.schema import CamelizedBaseStruct
 
from uuid import UUID

from db.models import OrderStatus
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
    expected_arrived_date:str | None = "" # ISO format saved for order expected arrived date

class OrderDetail(CamelizedBaseStruct):
    id:UUID
    user_id: UUID
    address:str
    total_price: float
    phone:str
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    handler_id: str|None
    order_products:list[OrderProduct]
    expected_arrived_date:str | None = "" # ISO format saved for order expected arrived date

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
    phone:str
    

class OrderUpdate(CamelizedBaseStruct):
    id:UUID
    order_status:OrderStatus
    handler_id:str
    expected_arrived_date:datetime

class OrderProduct(CamelizedBaseStruct):
    product_id:UUID
    quantity: int
    price_at_order:float
    discount_percent_at_order:float
 


