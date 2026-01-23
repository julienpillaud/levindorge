from app.domain.commons.category_groups import CategoryGroupName
from app.domain.commons.entities import InventoryGroup, PricingGroup
from app.domain.entities import DomainEntity


class Category(DomainEntity):
    name: str
    pricing_group: PricingGroup
    category_group: CategoryGroupName
    inventory_group: InventoryGroup
