from __future__ import annotations


from domain.lib.schema import CamelizedBaseStruct
from uuid import UUID 
from datetime import datetime

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
    created_at:datetime
    updated_at:datetime
    address: str|None = ""
    image_url: str|None = None
    is_superuser: bool = False
    is_active: bool = False
    is_verified: bool = False
 

class UserCreate(CamelizedBaseStruct):
    email: str
    password: str
    name: str
    is_superuser: bool = False
    is_active: bool = True
    is_verified: bool = False


class UserUpdate(CamelizedBaseStruct):
    old_password:str
    new_name: str|None = None
    new_password: str|None = None
    new_address:str|None = None
    new_image_url:str|None = None
    is_superuser: bool = False


class AccountLogin(CamelizedBaseStruct):
    email: str
    password: str

class APIAuth(CamelizedBaseStruct):
    username: str
    password: str

class AccountRegister(CamelizedBaseStruct):
    email: str
    password: str
    name: str 