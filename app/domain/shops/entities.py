from pydantic import BaseModel

from app.domain.entities import DomainModel


class ShopMargin(BaseModel):
    ratio: float
    operator: str
    decimal_round: float


class Shop(DomainModel):
    name: str
    username: str
    margins: dict[str, ShopMargin]
