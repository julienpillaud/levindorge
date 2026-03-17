from cleanstack.entities import DomainEntity

from app.domain.commons.category_groups import CategoryGroupName
from app.domain.commons.entities import InventoryGroup, PricingGroup


class Category(DomainEntity):
    name: str
    pricing_group: PricingGroup
    category_group: CategoryGroupName
    inventory_group: InventoryGroup
