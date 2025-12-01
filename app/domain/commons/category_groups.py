from enum import StrEnum

from pydantic import BaseModel

from app.domain._shared.entities import ProducerType
from app.domain.entities import DomainEntity


class CategoryGroupName(StrEnum):
    BEER = "beer"
    KEG = "keg"
    SPIRIT = "spirit"
    WINE = "wine"
    OTHER = "other"


class ProducerData(BaseModel):
    display_name: str
    type: ProducerType | None = None


class DepositField(BaseModel):
    unit: bool
    case: bool
    packaging: bool


class CategoryGroup(DomainEntity):
    name: CategoryGroupName
    producer: ProducerData | None
    origin: bool
    color: bool
    taste: bool
    volume: bool
    alcohol_by_volume: bool
    deposit: DepositField | None = None


CATEGORY_GROUPS_MAP = {
    CategoryGroupName.BEER: CategoryGroup(
        name=CategoryGroupName.BEER,
        producer=ProducerData(
            display_name="Brasserie",
            type=ProducerType.BREWERY,
        ),
        origin=True,
        color=True,
        taste=False,
        volume=True,
        alcohol_by_volume=True,
        deposit=DepositField(unit=True, case=True, packaging=True),
    ),
    CategoryGroupName.KEG: CategoryGroup(
        name=CategoryGroupName.KEG,
        producer=ProducerData(
            display_name="Brasserie",
            type=ProducerType.BREWERY,
        ),
        origin=True,
        color=True,
        taste=False,
        volume=True,
        alcohol_by_volume=True,
        deposit=DepositField(unit=True, case=False, packaging=False),
    ),
    CategoryGroupName.SPIRIT: CategoryGroup(
        name=CategoryGroupName.SPIRIT,
        producer=ProducerData(
            display_name="Distillerie",
            type=ProducerType.DISTILLERY,
        ),
        origin=True,
        color=False,
        taste=True,
        volume=True,
        alcohol_by_volume=True,
    ),
    CategoryGroupName.WINE: CategoryGroup(
        name=CategoryGroupName.WINE,
        producer=ProducerData(display_name="Appellation"),
        origin=True,
        color=True,
        taste=False,
        volume=True,
        alcohol_by_volume=False,
    ),
    CategoryGroupName.OTHER: CategoryGroup(
        name=CategoryGroupName.OTHER,
        producer=None,
        origin=False,
        color=False,
        taste=False,
        volume=False,
        alcohol_by_volume=False,
    ),
}
