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

 

class CustomerLevel(str , Enum):
    CLASSIC = "classic"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"