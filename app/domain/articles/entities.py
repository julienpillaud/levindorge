import datetime
from enum import StrEnum
from typing import Literal

from pydantic import (
    BaseModel,
    NonNegativeFloat,
    NonNegativeInt,
    PositiveFloat,
)

from app.domain.entities import DomainModel

LITER_TO_CENTILITER = 100


class ArticleColor(StrEnum):
    UNDEFINED = ""
    # beer
    AMBER_BEER = "Ambrée"
    WHITE_BEER = "Blanche"
    BLONDE_BEER = "Blonde"
    BROWN_BEER = "Brune"
    FRUITY_BEER = "Fruitée"
    # wine
    WHITE_WINE = "Blanc"
    ROSE_WINE = "Rosé"
    RED_WINE = "Rouge"


class ArticleTaste(StrEnum):
    UNDEFINED = ""
    OAKY = "Boisé"
    SPICY = "Epicé"
    FLORAL = "Floral"
    FRUITY = "Fruité"
    BRINY = "Iodé"
    TOASTY = "Toasté"
    PEATY = "Tourbé"
    HERBAL = "Végétal"


class ArticleName(BaseModel):
    name1: str
    name2: str


class ArticleVolume(BaseModel):
    value: PositiveFloat
    unit: Literal["cL", "L"]


class ArticleDeposit(BaseModel):
    unit: NonNegativeFloat
    case: NonNegativeFloat


class ArticleMargins(BaseModel):
    margin: NonNegativeFloat
    markup: NonNegativeFloat


class ArticleShop(BaseModel):
    sell_price: PositiveFloat
    bar_price: NonNegativeFloat
    stock_quantity: int
    recommended_price: PositiveFloat
    margins: ArticleMargins


class BaseArticle(BaseModel):
    type: str
    name: ArticleName
    buy_price: PositiveFloat
    excise_duty: NonNegativeFloat = 0.0
    social_security_levy: NonNegativeFloat = 0.0
    tax: float
    distributor: str
    barcode: str = ""
    region: str = ""
    color: ArticleColor = ArticleColor.UNDEFINED
    taste: ArticleTaste = ArticleTaste.UNDEFINED
    volume: ArticleVolume | None
    alcohol_by_volume: NonNegativeFloat = 0.0
    packaging: NonNegativeInt = 0
    deposit: ArticleDeposit
    food_pairing: list[str] = []
    biodynamic: str = ""

    @property
    def taxfree_price(self) -> float:
        taxfree_price_sum = sum(
            [self.buy_price, self.excise_duty, self.social_security_levy]
        )
        return round(taxfree_price_sum, 4)

    def formated_volume(self, /, separator: str = ".") -> str:
        if not self.volume:
            return ""

        value, unit = self.volume.value, self.volume.unit
        if unit == "cL" and value > LITER_TO_CENTILITER:
            value = value / 100
            unit = "L"

        formatted_value = str(value).rstrip("0").rstrip(".").replace(".", separator)
        return f"{formatted_value}{unit}"


class ArticleCreateOrUpdate(BaseArticle):
    shops: dict[str, ArticleShop]


class Article(DomainModel, BaseArticle):
    validated: bool
    created_by: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    shops: dict[str, ArticleShop]
