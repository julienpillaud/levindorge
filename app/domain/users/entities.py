from enum import StrEnum

from pydantic import BaseModel

from app.domain.entities import DomainModel
from app.domain.stores.entities import Store


class Role(StrEnum):
    USER = "user"
    ADMIN = "admin"
    SUPERUSER = "superuser"


class UserUpdate(BaseModel):
    hashed_password: str


class User(DomainModel):
    name: str
    username: str
    email: str
    hashed_password: str
    stores: list[Store]
    role: Role
