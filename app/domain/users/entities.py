from enum import StrEnum

from pydantic import BaseModel

from app.domain.entities import DomainEntity
from app.domain.stores.entities import Store


class Role(StrEnum):
    USER = "user"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class UserUpdate(BaseModel):
    hashed_password: str


class User(DomainEntity):
    name: str
    email: str
    hashed_password: str
    stores: list[Store]
    role: Role
