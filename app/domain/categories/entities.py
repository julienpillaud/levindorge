from app.domain.commons.entities import PricingGroup
from app.domain.entities import DomainModel


class Category(DomainModel):
    name: str
    pricing_group: PricingGroup
    tactill_category: str
