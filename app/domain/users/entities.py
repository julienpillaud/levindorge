from enum import StrEnum

from pydantic import BaseModel

from app.domain.entities import DomainModel
from app.domain.shops.entities import Shop


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
    shops: list[Shop]
    role: Role
