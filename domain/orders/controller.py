from __future__ import annotations

import os
 
from typing import Annotated, Any
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
from domain.orders.schemas import Order, OrderCreate, OrderProduct, OrderUpdate, OrderProductCreate, OrderDetail

from uuid import uuid4, UUID
from litestar.response import File
from urllib.parse import unquote

from logging import getLogger

logger = getLogger()

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
    ) -> dict[str, Any]:
   
        """Create a new Order."""
        order = data.to_dict()
        logger.info("ORDER data")
        logger.info(order)
        cart_products = order["order_products"]
 
        order_dict ={
            "address":order["address"],
            "phone": order["phone"],
            "total_price":order["total_price"],
            "user_id":current_user.id ,
            "status":OrderStatus.PENDING,
            "expected_arrived_date":""
        }

        order_obj:OrderModel = await order_service.create(data = order_dict)

        order_products:list[OrderProductCreate] = []
        try:
            for cart_product in cart_products:
                new_order_product = OrderProductCreate(
                order_id = order_obj.id,
                product_id= cart_product.product_id,
                quantity= cart_product.quantity,
                price_at_order=cart_product.price_at_order,
                discount_percent_at_order=cart_product.discount_percent_at_order
                )
                order_products.append(new_order_product)
            
            order_product_objs = await order_product_service.create_many(data=order_products)
            order_obj.order_products = order_product_objs

 
            order_products = order_product_service.to_schema(data=order_product_objs, total=len(order_product_objs), schema_type=OrderProduct)
                
            order = order_service.to_schema(data=order_obj,  schema_type=Order)
            order = order.to_dict()
            order.update({"order_products":order_products.items})

            return order

        except Exception as e:
            logger.error(e)
            await order_service.delete(item_id=order_obj.id)
            raise HTTPException(detail="Failed to create order", status_code=500)
    
       
 
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

        return order_service.to_schema(data=results, total=total, schema_type=Order, filters=filters)


    @get(path=urls.ORDER_DETAIL)
    async def get_order_detail(
        self,
        order_service: OrderService,
        order_product_service:OrderProductService,
        id: UUID = Parameter(
            title="Order ID",
            description="The Order to retrieve.",
        ),
    ) -> dict[str, Any]:
        """Get an existing Order."""
        order_obj = await order_service.get(item_id=id)
        order_product_objs = order_obj.order_products
        order_products = order_product_service.to_schema(data=order_product_objs, total=len(order_product_objs), schema_type=OrderProduct)
              
        order = order_service.to_schema(data=order_obj,  schema_type=OrderDetail)
        order = order.to_dict()
        order.update({"order_products":order_products.items})

        return order

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
 
