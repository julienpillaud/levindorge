from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


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
    OTHER = "other"


class ArticleType(BaseModel):
    name: str
    category: str
    tax: float
    pricing_group: PricingGroup = Field(alias="ratio_category")
    display_group: DisplayGroup = Field(alias="list_category")
    volume_category: str | None = None
    tactill_category: str


class ViewData(BaseModel):
    display_group: DisplayGroup
    pricing_group: PricingGroup
    article_type_names: list[str]
    items: dict[str, Any]
