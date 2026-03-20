from enum import StrEnum

from pydantic import BaseModel

from app.domain.metadata.entities.colors import ArticleColor
from app.domain.metadata.entities.deposits import Deposit
from app.domain.metadata.entities.distributors import Distributor
from app.domain.metadata.entities.origins import Origin
from app.domain.metadata.entities.producers import Producer
from app.domain.metadata.entities.volumes import ArticleVolume


class ArticleTaste(StrEnum):
    OAKY = "Boisé"
    SPICY = "Epicé"
    FLORAL = "Floral"
    FRUITY = "Fruité"
    BRINY = "Iodé"
    TOASTY = "Toasté"
    PEATY = "Tourbé"
    HERBAL = "Végétal"


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
    volumes: list[ArticleVolume]
    deposits: list[Deposit]
