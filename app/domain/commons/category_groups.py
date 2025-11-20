from enum import StrEnum

from pydantic import BaseModel

from app.domain.entities import DomainEntity


class CategoryGroupName(StrEnum):
    BEER = "beer"
    KEG = "keg"
    SPIRIT = "spirit"
    WINE = "wine"
    OTHER = "other"


class DepositField(BaseModel):
    case: bool
    unit: bool


class CategoryGroup(DomainEntity):
    name: CategoryGroupName
    producer: str
    product: str | None
    region: str | None
    color: bool
    taste: bool
    volume: bool
    alcohol_by_volume: bool

    # recommended_price: bool = True
    # distributor: bool = True
    # packaging: bool = False
    # deposit: DepositField | None = None


CATEGORY_GROUPS_MAP = {
    CategoryGroupName.BEER: CategoryGroup(
        name=CategoryGroupName.BEER,
        producer="Brasserie",
        product="Bière",
        region="Pays",
        color=True,
        taste=False,
        volume=True,
        alcohol_by_volume=True,
    ),
    CategoryGroupName.KEG: CategoryGroup(
        name=CategoryGroupName.KEG,
        producer="Brasserie",
        product="Bière",
        region="Pays",
        color=True,
        taste=False,
        volume=True,
        alcohol_by_volume=True,
    ),
    CategoryGroupName.SPIRIT: CategoryGroup(
        name=CategoryGroupName.SPIRIT,
        producer="Distillerie",
        product="Spiritueux",
        region="Pays",
        color=False,
        taste=True,
        volume=True,
        alcohol_by_volume=True,
    ),
    CategoryGroupName.WINE: CategoryGroup(
        name=CategoryGroupName.WINE,
        producer="Appellation",
        product="Vin",
        region="Région",
        color=True,
        taste=False,
        volume=True,
        alcohol_by_volume=False,
    ),
    CategoryGroupName.OTHER: CategoryGroup(
        name=CategoryGroupName.OTHER,
        producer="Désignation",
        product=None,
        region=None,
        color=False,
        taste=False,
        volume=False,
        alcohol_by_volume=False,
    ),
}
