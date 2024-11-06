from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from models import Product, User, Order, OrderProduct, Category, SubCategory
 

class UserRepository(SQLAlchemyAsyncRepository[User]):
    """User repository."""

    model_type = User



class ProductRepository(SQLAlchemyAsyncRepository[Product]):
    """User repository."""

    model_type = Product



class OrderRepository(SQLAlchemyAsyncRepository[Order]):
    """User repository."""

    model_type = Order