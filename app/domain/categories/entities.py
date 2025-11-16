from app.domain.commons.entities import PricingGroup
from app.domain.entities import DomainEntity


class Category(DomainEntity):
    name: str
    pricing_group: PricingGroup
    tactill_category: str
