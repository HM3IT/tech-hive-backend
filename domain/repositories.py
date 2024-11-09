from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from db.models import Product, User, Order, Category, SubCategory
 

class UserRepository(SQLAlchemyAsyncRepository[User]):
    """User repository."""

    model_type = User



class ProductRepository(SQLAlchemyAsyncRepository[Product]):
    """User repository."""

    model_type = Product



class OrderRepository(SQLAlchemyAsyncRepository[Order]):
    """User repository."""

    model_type = Order



class CategoryRepository(SQLAlchemyAsyncRepository[Category]):
    """User repository."""

    model_type = Category



class SubCategoryRepository(SQLAlchemyAsyncRepository[SubCategory]):
    """User repository."""

    model_type = SubCategory