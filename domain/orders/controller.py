from __future__ import annotations

from uuid import UUID
from typing import Annotated, Any, Optional
from litestar import get, post, patch

from litestar.params import Dependency, Parameter
from litestar.exceptions import HTTPException
from litestar.controller import Controller
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.repository.filters import LimitOffset, CollectionFilter

from db.models import User, Order as OrderModel, OrderStatus

from domain.orders import urls
from domain.orders.services import OrderService, OrderProductService
from domain.orders.dependencies  import provide_order_service, provide_ordered_product_service
from domain.orders.schemas import Order, OrderCreate, OrderProduct, OrderUpdate, OrderProductCreate, OrderDetail

from domain.users.guards import requires_active_user, requires_superuser

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


    @post(path=urls.ORDER_ADD)
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
        logger.info("order info")
        logger.info(order_dict)
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

            logger.info("order_products")
            logger.info(order_products)
            
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
    
       
 
    @get(path=urls.ORDER_ADMIN_LIST, guards=[requires_superuser],  cache=60)
    async def list_order(
        self,
        order_service: OrderService,
        order_product_service:OrderProductService,
        # limit_offset: LimitOffset,
        filters: Annotated[CollectionFilter, Dependency(skip_validation=True)] = None,
        user_id: Optional[UUID] = None
    ) -> OffsetPagination[Order]:
        """List orders."""
        filters = filters or []
        if user_id:
     
            results, total = await order_service.list_and_count(CollectionFilter("user_id", [user_id]))
        else:
            results, total = await order_service.list_and_count(*filters)

        return order_service.to_schema(data=results, total=total, schema_type=Order, filters=filters)


    @get(path=urls.ORDER_LIST)
    async def list_my_order(
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
        order_dict = order.to_dict()
        order_dict.update({"order_products":order_products.items})

        return order_dict

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
        order_id = order["id"]
        order_obj = order_service.get_one_or_none(id=order_id)
        if order_obj is None:
            raise HTTPException(detail="Order Not Found", status_code = 404)

        expected_order_date = order["expected_arrived_date"]
        iso_format_order = expected_order_date.isoformat()
        order["expected_arrived_date"] = iso_format_order
      
      
        status_enum = OrderStatus(order["order_status"])
        update_order_data = {
            "status":status_enum,
            "expected_arrived_date":iso_format_order,
            "handler_id":order["handler_id"]
        }

        db_obj = await order_service.update(item_id= order_id, data=update_order_data)
        return order_service.to_schema(db_obj, schema_type=Order)
