from pydantic import Field

from app.domain.entities import DomainModel


class User(DomainModel):
    name: str
    username: str
    email: str
    hashed_password: str = Field(alias="password")
