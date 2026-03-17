from cleanstack.entities import DomainEntity
from pydantic import BaseModel


class User(DomainEntity):
    email: str


class UserCredentials(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int


class UserWithCredentials(User):
    credentials: UserCredentials
