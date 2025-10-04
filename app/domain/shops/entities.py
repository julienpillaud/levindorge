from typing import Literal

from pydantic import BaseModel

from app.domain.entities import DomainModel


class ShopMargin(BaseModel):
    ratio: float
    operator: Literal["+", "*"]
    decimal_round: float


class Shop(DomainModel):
    name: str
    username: str
    tactill_api_key: str
    margins: dict[str, ShopMargin]
