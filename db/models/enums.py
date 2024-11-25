from enum import Enum

class UserType(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class OrderStatus(str , Enum):
    PENDING = "pending"
    CONFIRM = "confirm"
    CANCELLED = "cancelled"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

class Tags(str, Enum):
    NEW_ARRIVAL = "New Arrival"
    FLASH_SALE = "Flash Sales"
    PROMOTION = "Promotion"
    BEST_SELLER = "Best Seller"
    DISCOUNTED = "Discounted"
    TRENDING = "Trending"
    PRE_ORDER = "Pre-order"
    FREE_SHIPPING = "Free Shipping"
    GIFT_IDEAS = "Gift Ideas"
    CUSTOMER_FAVORITE = "Customer Favorite"
    HIGHLY_RATED = "Highly Rated"

class CustomerLevel(str , Enum):
    CLASSIC = "classic"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"