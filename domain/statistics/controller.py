from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Annotated, Any
from litestar.params import Dependency, Parameter
from litestar import get, post, patch
from litestar.exceptions import HTTPException
from litestar.controller import Controller
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.repository.filters import LimitOffset
from domain.orders.dependencies  import provide_order_service, provide_ordered_product_service
from domain.products.depedencies import provide_product_service
from domain.orders.services import OrderService, OrderProductService
from domain.products.services import ProductService
from domain.users.services import UserService
from domain.statistics import urls
from domain.users.guards import requires_active_user, requires_superuser
from litestar.repository.filters import CollectionFilter
from db.models import User, Order as OrderModel, OrderStatus, OrderProduct as OrderProductModel, User as UserModel, Product as ProductModel
from domain.orders.schemas import Order, OrderCreate, OrderProduct, OrderUpdate, OrderProductCreate, OrderDetail

from logging import getLogger

logger = getLogger()

class StatisticController(Controller):
    """Statisitc API for admin dashbaord"""
    tags = ["Statistics"]
    dependencies = {
        "product_service": Provide(provide_product_service),
        "order_service": Provide(provide_order_service),
        "order_product_service":Provide(provide_ordered_product_service)
    }
    guards = [requires_active_user, requires_superuser]


    @get(path=urls.ALL_TOTAL)
    async def get_total_statistics(
        self,
        product_service: ProductService,
        order_service: OrderService,
        user_service:UserService,
        filters: Annotated[CollectionFilter, Dependency(skip_validation=True)] = None,
        filter_date:datetime | None = None,
    ) -> dict[str, float]:
        """Monthly Revenue Statistics"""
        if filter_date is None:
            filter_date = datetime.now(timezone.utc)
        
        start_date = datetime(filter_date.year, filter_date.month, 1, tzinfo=timezone.utc)
 
        next_month = filter_date.replace(month=filter_date.month % 12 + 1, day=1)
        end_date = next_month - timedelta(days=1)

 
        filters = [
            OrderModel.created_at >= start_date,
            OrderModel.created_at <= end_date,
        ]

  
        orders, order_total = await order_service.list_and_count(*filters)
        products, product_total = await product_service.list_and_count()
        users, user_total = await user_service.list_and_count(*filters)


        revenue = sum(float(order.total_price) for order in orders)
        expense = sum(float(product.price * product.stock) for product in products)

   
        if expense > 0:
            profit_margin = (revenue - expense) / expense * 100
        else:
            profit_margin = 0.0  
      

        return {
            "revenue": revenue,
            "expense": expense,
            "profit_margin": profit_margin,
            "products":product_total,
            "orders":order_total,
            "users": user_total,
        }

    @get(path=urls.ORDER_SALES_TREND_WEEKLY)
    async def get_weekly_order_trend(
        self,
        product_service: ProductService,
        order_service: OrderService,
        user_service:UserService,
        filter_date:datetime | None = None,
    ) -> dict[str, Any]:
        """Weekly Order Trend"""
 
        if filter_date is None:
            filter_date = datetime.now(timezone.utc)
  
        start_date = filter_date - timedelta(days=6)  

 
        logger.info(f"Weekly range: {start_date} to {filter_date}")
 
        filters = [
            OrderModel.created_at >= start_date,
            OrderModel.created_at <= filter_date,
        ]
        orders, order_total = await order_service.list_and_count(*filters)
 
        daily_data = {}
        for order in orders:
            order_date = order.created_at.date()  
            if order_date not in daily_data:
                daily_data[order_date] = 0
            daily_data[order_date] += 1 

        order_trend = [
            {"date": date.isoformat(), "count": count}
            for date, count in sorted(daily_data.items()) 
        ]

        return {
            "trend": order_trend,
            "total_count": order_total,
            "date_range": {"start_date": start_date.isoformat(), "end_date": filter_date.isoformat()},
        }
