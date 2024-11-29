from __future__ import annotations
from datetime import date
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
from domain.categories.depedencies import provide_category_service
from domain.orders.services import OrderService, OrderProductService
from domain.products.services import ProductService
from domain.users.services import UserService
from domain.categories.services import CategoryService
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
        "order_product_service":Provide(provide_ordered_product_service),
        "category_service":Provide(provide_category_service)
    }
    guards = [requires_active_user, requires_superuser]


    @get(path=urls.ALL_TOTAL)
    async def get_total_statistics(
        self,
        product_service: ProductService,
        order_service: OrderService,
        user_service:UserService,
        filters: Annotated[CollectionFilter, Dependency(skip_validation=True)] = None,
        filter_date:date | None = None,
    ) -> dict[str, float]:
        """Monthly Revenue Statistics"""
        if filter_date is None:
            filter_date = datetime.now(timezone.utc).date()

        start_date = datetime(filter_date.year, filter_date.month, 1, tzinfo=timezone.utc)

        if filter_date.month == 12:
            next_month = datetime(filter_date.year + 1, 1, 1, tzinfo=timezone.utc)
        else:
            next_month = datetime(filter_date.year, filter_date.month + 1, 1, tzinfo=timezone.utc)

        end_date = next_month - timedelta(seconds=1)
 
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
        filter_date:date | None = None,
    ) -> dict[str, Any]:
        """Weekly Order Trend"""
 
        if filter_date is None:
            filter_date = datetime.now(timezone.utc).date()

       
        week_start = filter_date - timedelta(days=filter_date.weekday())  
        week_end = week_start + timedelta(days=6)   

  
        start_date = datetime(week_start.year, week_start.month, week_start.day, tzinfo=timezone.utc)
        end_date = datetime(week_end.year, week_end.month, week_end.day, 23, 59, 59, tzinfo=timezone.utc)
 
        logger.info(f"Weekly range: {start_date} to {end_date}")
 
        filters = [
            OrderModel.created_at >= start_date,
            OrderModel.created_at <= end_date,
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



    @get(path=urls.CATEGORY_WISE_REVENUE)
    async def get_category_wise_revenue(
        self,
        product_service: ProductService,
        category_service: CategoryService,
        order_product_service: OrderProductService,
        filter_date: date | None = None,
    ) -> dict[str, Any]:
        """Category-wise revenue"""

        if filter_date is None:
            filter_date = datetime.now(timezone.utc).date()

        start_date = datetime(filter_date.year, filter_date.month, 1, tzinfo=timezone.utc)

        if filter_date.month == 12:
            next_month = datetime(filter_date.year + 1, 1, 1, tzinfo=timezone.utc)
        else:
            next_month = datetime(filter_date.year, filter_date.month + 1, 1, tzinfo=timezone.utc)

        end_date = next_month - timedelta(seconds=1)

        logger.info(f"Filtered date range: {start_date} to {end_date}")
 
        categories, category_total = await category_service.list_and_count()
 
        category_trend = []
        for category in categories:
      
            revenue = 0.0
            quantity = 0
            for product in category.products:
                order_items, _ = await order_product_service.list_and_count(
                    OrderProductModel.product_id == product.id,
                    OrderProductModel.created_at >= start_date,
                    OrderProductModel.created_at <= end_date,
                )
                for item in order_items:
                    revenue += int(item.quantity) * float(item.price_at_order)
                    quantity += int(item.quantity)
 
            category_trend.append({
                "name": category.name,
                "revenue": revenue,
                "sold":quantity
            })
 
        return {
            "trend": category_trend,
            "total_count": category_total,
            "date_range": {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()},
        }


    @get(path=urls.TREND_PRODUCT_MONTHLY)
    async def get_trending_products(
        self,
        product_service: ProductService,
        order_product_service: OrderProductService,
        filter_date: date | None = None,
    ) -> dict[str, Any]:
        """Trending Products"""

        if filter_date is None:
            filter_date = datetime.now(timezone.utc).date()

        start_date = datetime(filter_date.year, filter_date.month, 1, tzinfo=timezone.utc)

        if filter_date.month == 12:
            next_month = datetime(filter_date.year + 1, 1, 1, tzinfo=timezone.utc)
        else:
            next_month = datetime(filter_date.year, filter_date.month + 1, 1, tzinfo=timezone.utc)
    
        end_date = next_month - timedelta(seconds=1)

        logger.info(f"Filtered date range: {start_date} to {end_date}")

        order_items, _ = await order_product_service.list_and_count(
            OrderProductModel.created_at >= start_date,
            OrderProductModel.created_at <= end_date,
        )

        trend_products = {}
 
        for item in order_items:
            if item.product_id not in trend_products:
                product_obj = await product_service.get(item_id=item.product_id)
                trend_products[item.product_id] = {
                    "id": product_obj.id,
                    "name": product_obj.name,
                    "image_url": product_obj.image_url,
                    "revenue": 0.0,
                    "sold": 0,
                    "stock":product_obj.stock
                }

    
            trend_products[item.product_id]["revenue"] += float(item.price_at_order) * int(item.quantity)
            trend_products[item.product_id]["sold"] += int(item.quantity)

        # Sorting products by quantity sold and return only the top 10 products
        sorted_trend_products = sorted(trend_products.values(), key=lambda x:x["sold"], reverse=True)[:5]

        return {
            "trend": sorted_trend_products,
            "total_count": len(sorted_trend_products),
            "date_range": {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()},
        }
