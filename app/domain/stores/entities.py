from typing import Literal

from pydantic import BaseModel

from app.domain.commons.entities import PricingGroup
from app.domain.entities import DomainModel


class PricingConfig(BaseModel):
    value: float
    operator: Literal["+", "*"]
    round_step: float


class Store(DomainModel):
    name: str
    slug: str
    tactill_api_key: str
    pricing_configs: dict[PricingGroup, PricingConfig]
