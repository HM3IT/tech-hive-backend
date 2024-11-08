from __future__ import annotations

from uuid import UUID 
from domain.lib.schema import CamelizedBaseStruct
from domain.orders.schema import Order

__all__ = (
    "AccountLogin",
    "AccountRegister",
    "UserCreate",
    "User",
    "UserUpdate",
)

class User(CamelizedBaseStruct):
    """User properties to use for a response."""

    id: UUID
    email: str
    name: str
    user_level:str
    address: str|None = None
    image_url: str|None = None
    is_superuser: bool = False
    is_active: bool = False
    is_verified: bool = False
    orders: list[Order] = []
 

class UserCreate(CamelizedBaseStruct):
    email: str
    password: str
    name: str
    is_superuser: bool = False
    is_active: bool = True
    is_verified: bool = False


class UserUpdate(CamelizedBaseStruct, omit_defaults=True):
    email: str | None 
    password: str | None
    name: str | None
    is_superuser: bool | None 
    is_active: bool | None 
    is_verified: bool | None 


class AccountLogin(CamelizedBaseStruct):
    name: str
    password: str


class AccountRegister(CamelizedBaseStruct):
    email: str
    password: str
    name: str | None = None

 