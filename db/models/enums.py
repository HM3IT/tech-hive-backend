from enum import Enum

class UserType(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class OrderStatus(str , Enum):
    PENDING = "pending"
    CONFIRM = "confirm"
    CANCEL = "cancel"
    REJECT = "reject"
    DELIVERED = "delivered"

class CustomerLevel(str , Enum):
    CLASSIC = "classic"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"