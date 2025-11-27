from app.domain._shared.entities import ProducerType
from app.domain.commons.category_groups import CategoryGroupName
from app.domain.commons.entities import PricingGroup
from app.domain.deposits.entities import DepositCategory
from app.domain.entities import DomainEntity
from app.domain.volumes.entities import VolumeCategory


class Category(DomainEntity):
    name: str
    pricing_group: PricingGroup
    category_group: CategoryGroupName
    producer_type: ProducerType | None = None
    volume_category: VolumeCategory | None = None
    deposit_category: DepositCategory | None = None
    tactill_category: str
