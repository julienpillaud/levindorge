from decimal import ROUND_CEILING, ROUND_HALF_EVEN
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.domain.commons.entities import PricingGroup
from app.domain.entities import DomainEntity
from app.domain.types import DecimalType, StoreName, StoreSlug


class RoundingMode(Enum):
    ROUND_HALF_EVEN = ROUND_HALF_EVEN
    ROUND_CEILING = ROUND_CEILING


class RoundConfig(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    value: DecimalType
    rounding_mode: RoundingMode


class PricingConfig(BaseModel):
    value: DecimalType
    operator: Literal["+", "*"]
    round_config: RoundConfig


class Store(DomainEntity):
    name: StoreName
    slug: StoreSlug
    tactill_api_key: str
    pricing_configs: dict[PricingGroup, PricingConfig]
