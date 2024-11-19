from __future__ import annotations

from domain.lib.schema import CamelizedBaseStruct
from db.models import OrderStatus
from domain.users.schemas import User
from domain.products.schemas import Product
from uuid import UUID


class Order(CamelizedBaseStruct):
 
    user_id: UUID
    address:str
    total_price: float
    status: OrderStatus
    user: User
    products: list[OrderProduct]


class OrderCreate(CamelizedBaseStruct):
    pass

class OrderUpdate(CamelizedBaseStruct):
    id:UUID
    order_status:OrderStatus

class OrderProduct(CamelizedBaseStruct):
    product:Product
    order_id: UUID
    quantity: int
    price_at_order:float
    discount_at_order:float
    