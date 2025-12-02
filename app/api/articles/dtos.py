from typing import Any

from pydantic import BaseModel, field_validator, model_validator

from app.domain.articles.entities import (
    ArticleDeposit,
    ArticleStoreData,
    ArticleVolume,
)
from app.domain.articles.utils import (
    extract_deposit,
    extract_shops,
    extract_volume,
)
from app.domain.commons.entities import PricingGroup
from app.domain.types import DecimalType, StoreSlug


class PriceRequestDTO(BaseModel):
    total_cost: DecimalType
    vat_rate: DecimalType
    pricing_group: PricingGroup


class MarginsRequestDTO(BaseModel):
    total_cost: DecimalType
    vat_rate: DecimalType
    gross_price: DecimalType


class ArticleDTO(BaseModel):
    producer: str | None
    product: str
    cost_price: float
    excise_duty: float = 0.0
    social_security_contribution: float = 0.0
    vat_rate: float
    distributor: str
    barcode: str = ""
    origin: str | None = None
    color: str | None = None
    taste: str | None = None
    volume: ArticleVolume | None = None
    alcohol_by_volume: float | None = None
    deposit: ArticleDeposit | None = None
    store_data: dict[StoreSlug, ArticleStoreData]

    @model_validator(mode="before")
    @classmethod
    def extract_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        extract_volume(data)
        extract_deposit(data)
        extract_shops(data)
        return data

    @field_validator(
        "excise_duty",
        "social_security_contribution",
        mode="before",
    )
    @classmethod
    def empty_string_to_zero(cls, value: str) -> float:
        return float(value) if value else 0.0

    @field_validator(
        "producer",
        "origin",
        "color",
        "taste",
        "alcohol_by_volume",
        mode="before",
    )
    @classmethod
    def empty_string_to_none(cls, value: str) -> str | None:
        return value or None
