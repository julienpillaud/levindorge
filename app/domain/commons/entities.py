from enum import StrEnum

from pydantic import BaseModel

from app.domain.articles.entities import ArticleColor, ArticleTaste
from app.domain.deposits.entities import Deposit
from app.domain.distributors.entities import Distributor
from app.domain.origins.entities import Origin
from app.domain.producers.entities import Producer
from app.domain.volumes.entities import Volume


class InventoryGroup(StrEnum):
    BEER = "Bière"
    CIDER = "Cidre"
    KEG = "Fût"
    MINI_KEG = "Mini-fût"
    RUM = "Rhum"
    WHISKY = "Whisky"
    ARRANGED = "Arrangé"
    SPIRIT = "Spiritueux"
    WINE = "Vin"
    FORTIFIED_WINE = "Vin muté"
    SPARKLING_WINE = "Vin effervescent"
    BIB = "BIB"
    BOX = "Coffret"
    FOOD = "Alimentation / BSA"
    OTHER = "Accessoire / Emballage"


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


class ViewData(BaseModel):
    producers: list[Producer]
    distributors: list[Distributor]
    colors: list[ArticleColor]
    tastes: list[ArticleTaste]
    origins: list[Origin]
    volumes: list[Volume]
    deposits: list[Deposit]
