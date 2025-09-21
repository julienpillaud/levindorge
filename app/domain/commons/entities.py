from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.domain.entities import DomainModel


class DisplayGroup(StrEnum):
    BEER = "beer"
    CIDER = "cider"
    KEG = "keg"
    MINI_KEG = "mini_keg"
    RHUM = "rhum"
    WHISKY = "whisky"
    ARRANGED = "arranged"
    SPIRIT = "spirit"
    WINE = "wine"
    FORTIFIED_WINE = "fortified_wine"
    SPARKLING_WINE = "sparkling_wine"
    BIB = "bib"
    BOX = "box"
    FOOD = "food"
    MISC = "misc"


class PricingGroup(StrEnum):
    BEER = "beer"
    KEG = "keg"
    MINI_KEG = "mini_keg"
    SPIRIT = "spirit"
    ARRANGED = "arranged"
    WINE = "wine"
    BIB = "bib"
    BOX = "box"
    OTHERS = "others"


class ArticleType(BaseModel):
    name: str
    category: str
    tax: float
    pricing_group: PricingGroup = Field(alias="ratio_category")
    display_group: DisplayGroup = Field(alias="list_category")
    volume_category: str | None = None
    tactill_category: str


class Item(DomainModel):
    name: str
    demonym: str = ""


class Volume(DomainModel):
    value: float
    unit: Literal["cL", "L"]
    category: str


class Deposit(DomainModel):
    category: Literal["Bière", "Fût", "Mini-fût"]
    deposit_type: Literal["Unitaire", "Caisse"]
    value: float


class ViewData(BaseModel):
    display_group: DisplayGroup
    pricing_group: PricingGroup
    article_type_names: list[str]
    items: dict[str, Any]
