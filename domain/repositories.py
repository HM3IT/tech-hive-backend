from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from db.models import Product, User, Order, OrderProduct, Category, Tags, ProductTags, ProductReview
 

class UserRepository(SQLAlchemyAsyncRepository[User]):
    """User repository."""

    model_type = User


class ProductRepository(SQLAlchemyAsyncRepository[Product]):
    """Product repository."""

    model_type = Product


class CategoryRepository(SQLAlchemyAsyncRepository[Category]):
    """Category repository."""

    model_type = Category

class OrderRepository(SQLAlchemyAsyncRepository[Order]):
    """Order repository."""

    model_type = Order

class OrderProductRepository(SQLAlchemyAsyncRepository[OrderProduct]):
    """OrderProduct repository."""

    model_type = OrderProduct


class TagRepository(SQLAlchemyAsyncRepository[Tags]):
    """Tags repository."""

    model_type = Tags


class ProductTagRepository(SQLAlchemyAsyncRepository[ProductTags]):
    """ProductTags repository."""

    model_type = ProductTags


class ProductReviewRepository(SQLAlchemyAsyncRepository[ProductReview]):
    """ProductReview repository."""

    model_type = ProductReview
