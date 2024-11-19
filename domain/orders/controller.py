from __future__ import annotations

import os
 
from typing import Annotated
from litestar.params import Body
from litestar import get, post, delete, patch, Response, Request, MediaType
from litestar.exceptions import HTTPException
from litestar.controller import Controller
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from litestar.repository.filters import LimitOffset
from domain.orders.dependencies  import provide_order_service, provide_ordered_product_service
from domain.orders.services import OrderService, OrderProductService
from domain.orders import urls
from domain.users.guards import requires_active_user, requires_superuser
from litestar.repository.filters import CollectionFilter

from db.models import User, Order as OrderModel, OrderStatus, OrderProduct as OrderProductModel
from domain.orders.schemas import Order, OrderCreate, OrderProduct, OrderUpdate, OrderProductCreate

from uuid import uuid4, UUID
from litestar.response import File
from urllib.parse import unquote

from logging import getLogger

class OrderController(Controller):
    """Order CRUD"""
    tags = ["Order"]
    dependencies = {
        "order_service": Provide(provide_order_service),
        "order_product_service":Provide(provide_ordered_product_service)
        }
    guards=[requires_active_user]


    @post(path=urls.ORDER_ADD, guards=[requires_superuser, requires_active_user])
    async def create_order(
        self,
        order_service: OrderService,
        order_product_service:OrderProductService,
        data: OrderCreate,
        current_user:User
    ) -> Order:
   
        """Create a new Order."""
        order = data.to_dict()
        order_products = order["orderProducts"]
 
        order_dict ={
            "address":order["address"],
            "total_price":order["totalPrice"],
            "user_id":current_user.id ,
            "status":OrderStatus.PENDING
        }

        order_obj:OrderModel = await order_service.create(data = order_dict )
        order_products = [order_product.update({"order_id":order_obj.id}) for order_product in order_products]
        order_product_objs = await order_product_service.create_many(data=order_products)
        order_products = order_product_service.to_schema(data=order_product_objs, total= len(order_product_objs), schema_type=OrderProduct)

        return Order(
            user_id= current_user.id,
            address= order_obj.address,
            total_price= order_obj.total_price,
            status = order_obj.status,
            products = order_products
        )
 
    @get(path=urls.ORDER_LIST)
    async def list_order(
        self,
        order_service: OrderService,
        order_product_service:OrderProductService,
        limit_offset: LimitOffset,
        current_user: User,
    ) -> OffsetPagination[Order]:
        """List orders."""
        filters = [
            CollectionFilter("user_id", [current_user.id]),
            limit_offset
        ]
        results, total = await order_service.list_and_count(*filters)

        for order in results:
            ordered_products, total = await order_product_service.list_and_count(order_id=order.id)
            order_product_service.to_schema(data=ordered_products, total= total, schema_type=OrderProduct)
             

        return order_service.to_schema(data=results, total=total, schema_type=Order, filters=filters)



    @get(path=urls.ORDER_DETAIL)
    async def get_order(
        self,
        order_service: OrderService,
        id: UUID = Parameter(
            title="Order ID",
            description="The Order to retrieve.",
        ),
    ) -> Order:
        """Get an existing Order."""
        obj = await order_service.get(item_id=id)
              
        return order_service.to_schema(data=obj,  schema_type=Order)

    @patch(
        path=urls.ORDER_STATUS_UPDATE, guards=[requires_superuser, requires_active_user]
    )
    async def update_order(
        self,
        order_service: OrderService,
        data:OrderUpdate
    ) -> Order:
        """Update an Order."""
        order = data.to_dict()
        item_id = order["id"]
        order_status:OrderStatus = order["orderStatus"]
        if item_id is None:
            raise HTTPException(detail="Order Id must be included", status_code = 400)
        db_obj = await order_service.update(item_id=item_id, data={"order_status":order_status})
        return order_service.to_schema(db_obj, schema_type=Order)
 
