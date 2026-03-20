import json
from collections import defaultdict
from typing import Any

from pydantic import BaseModel, field_validator, model_validator

from app.domain.articles.entities import ArticleStoreData
from app.domain.commons.entities import PricingGroup
from app.domain.metadata.entities.deposits import ArticleDeposit
from app.domain.metadata.entities.origins import ArticleOrigin
from app.domain.metadata.entities.volumes import ArticleVolume
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
    category: str
    producer: str | None = None
    product: str
    cost_price: float
    excise_duty: float = 0.0
    social_security_contribution: float = 0.0
    vat_rate: float
    distributor: str
    barcode: str = ""
    origin: ArticleOrigin | None
    color: str | None = None
    taste: str | None = None
    volume: ArticleVolume | None
    alcohol_by_volume: float | None = None
    deposit: ArticleDeposit | None
    store_data: dict[StoreSlug, ArticleStoreData]

    @model_validator(mode="before")
    @classmethod
    def extract_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        extract_origin(data)
        extract_volume(data)
        extract_deposit(data)
        extract_store_data(data)
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
        "color",
        "taste",
        "alcohol_by_volume",
        mode="before",
    )
    @classmethod
    def empty_string_to_none(cls, value: str) -> str | None:
        return value or None


def extract_origin(data: dict[str, Any], /) -> None:
    origin_data = data.pop("origin", None)
    if not origin_data:
        data["origin"] = None
        return

    try:
        origin = json.loads(origin_data)
        data["origin"] = origin
    except json.decoder.JSONDecodeError as error:
        raise ValueError("Invalid origin data") from error


def extract_volume(data: dict[str, Any], /) -> None:
    volume_data = data.pop("volume", None)
    if not volume_data:
        data["volume"] = None
        return

    try:
        volume = json.loads(volume_data)
        data["volume"] = volume
    except json.decoder.JSONDecodeError as error:
        raise ValueError("Invalid volume data") from error


def extract_deposit(data: dict[str, Any], /) -> None:
    unit = data.pop("deposit.unit", None)
    if not unit:
        data["deposit"] = None
        return

    case = data.pop("deposit.case", None)
    packaging = data.pop("deposit.packaging", None)

    data["deposit"] = {
        "unit": float(unit),
        "case": float(case) if case else None,
        "packaging": float(packaging) if packaging else None,
    }


def extract_store_data(data: dict[str, Any], /) -> None:
    store_data: dict[str, dict[str, Any]] = defaultdict(dict)

    for key, value in data.items():
        if "store_data" not in key:
            continue

        parts = key.split(".")
        store_slug = parts[1]
        if "margins" in parts:
            store_data[store_slug].setdefault("margins", {})
            store_data[store_slug]["margins"][parts[3]] = float(value)
            continue
        store_data[store_slug][parts[2]] = float(value) if value else 0

    data["store_data"] = store_data
