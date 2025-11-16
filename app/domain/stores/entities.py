from typing import Literal

from pydantic import BaseModel

from app.domain.commons.entities import PricingGroup
from app.domain.entities import DomainEntity

type StoreSlug = str


class PricingConfig(BaseModel):
    value: float
    operator: Literal["+", "*"]
    round_step: float


class Store(DomainEntity):
    name: str
    slug: StoreSlug
    tactill_api_key: str
    pricing_configs: dict[PricingGroup, PricingConfig]
