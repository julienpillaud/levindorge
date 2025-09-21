from typing import Any

from pydantic import BaseModel, field_validator, model_validator

from app.domain.articles.entities import (
    ArticleDeposit,
    ArticleName,
    ArticleShop,
    ArticleVolume,
)
from app.domain.articles.utils import (
    extract_deposit,
    extract_name,
    extract_shops,
    extract_volume,
)


class PriceRequestDTO(BaseModel):
    ratio_category: str
    taxfree_price: float
    tax: float


class MarginsRequestDTO(BaseModel):
    taxfree_price: float
    tax: float
    sell_price: float


class ArticleDTO(BaseModel):
    type: str
    name: ArticleName
    buy_price: float
    excise_duty: float = 0.0
    social_security_levy: float = 0.0
    tax: float
    distributor: str
    barcode: str = ""
    region: str = ""
    color: str = ""
    taste: str = ""
    volume: ArticleVolume | None
    alcohol_by_volume: float = 0.0
    packaging: int = 0
    deposit: ArticleDeposit
    food_pairing: list[str] = []
    biodynamic: str = ""
    shops: dict[str, ArticleShop]

    @model_validator(mode="before")
    @classmethod
    def extract_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        extract_name(data)
        extract_volume(data)
        extract_deposit(data)
        extract_shops(data)
        return data

    @field_validator("excise_duty", "social_security_levy", mode="before")
    @classmethod
    def empty_string_to_zero(cls, value: str) -> float:
        return float(value) if value else 0.0
