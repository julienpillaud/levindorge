from pydantic import BaseModel

from app.domain.entities import DomainEntity


class User(DomainEntity):
    email: str


class UserCredentials(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int


class UserWithCredentials(User):
    credentials: UserCredentials
