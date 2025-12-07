from enum import StrEnum

from pydantic import BaseModel

from app.domain.deposits.entities import DepositCategory
from app.domain.entities import DomainEntity
from app.domain.producers.entities import ProducerType
from app.domain.volumes.entities import VolumeCategory


class CategoryGroupName(StrEnum):
    BEER = "beer"
    KEG = "keg"
    SPIRIT = "spirit"
    WINE = "wine"
    OTHER = "other"


class ProducerData(BaseModel):
    display_name: str
    type: ProducerType | None = None


class DepositData(BaseModel):
    unit: bool
    case: bool
    packaging: bool
    category: DepositCategory


class CategoryGroup(DomainEntity):
    name: CategoryGroupName
    display_name: str
    producer: ProducerData | None
    origin: bool
    color: bool
    taste: bool
    volume: VolumeCategory | None = None
    alcohol_by_volume: bool
    deposit: DepositData | None = None


CATEGORY_GROUPS_MAP = {
    CategoryGroupName.BEER: CategoryGroup(
        name=CategoryGroupName.BEER,
        display_name="Bière / Cidre",
        producer=ProducerData(
            display_name="Brasserie",
            type=ProducerType.BREWERY,
        ),
        origin=True,
        color=True,
        taste=False,
        volume=VolumeCategory.BEER,
        alcohol_by_volume=True,
        deposit=DepositData(
            unit=True,
            case=True,
            packaging=True,
            category=DepositCategory.BEER,
        ),
    ),
    CategoryGroupName.KEG: CategoryGroup(
        name=CategoryGroupName.KEG,
        display_name="Fût / Mini-fût",
        producer=ProducerData(
            display_name="Brasserie",
            type=ProducerType.BREWERY,
        ),
        origin=True,
        color=True,
        taste=False,
        volume=VolumeCategory.KEG,
        alcohol_by_volume=True,
        deposit=DepositData(
            unit=True,
            case=False,
            packaging=False,
            category=DepositCategory.KEG,
        ),
    ),
    CategoryGroupName.SPIRIT: CategoryGroup(
        name=CategoryGroupName.SPIRIT,
        display_name="Spiritueux",
        producer=ProducerData(
            display_name="Distillerie",
            type=ProducerType.DISTILLERY,
        ),
        origin=True,
        color=False,
        taste=True,
        volume=VolumeCategory.SPIRIT,
        alcohol_by_volume=True,
    ),
    CategoryGroupName.WINE: CategoryGroup(
        name=CategoryGroupName.WINE,
        display_name="Vin",
        producer=ProducerData(display_name="Appellation"),
        origin=True,
        color=True,
        taste=False,
        volume=VolumeCategory.WINE,
        alcohol_by_volume=False,
    ),
    CategoryGroupName.OTHER: CategoryGroup(
        name=CategoryGroupName.OTHER,
        display_name="Autre",
        producer=None,
        origin=False,
        color=False,
        taste=False,
        alcohol_by_volume=False,
    ),
}
