from pydantic import BaseModel

from app.domain.commons.entities import PricingGroup
from app.domain.stores.entities import PricingConfig
from app.domain.types import StoreSlug


class StoreDTO(BaseModel):
    id: str
    name: str
    slug: StoreSlug
    pricing_configs: dict[PricingGroup, PricingConfig]
