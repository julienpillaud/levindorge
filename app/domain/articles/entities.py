import datetime
from enum import StrEnum
from typing import Literal

from pydantic import (
    BaseModel,
    NonNegativeFloat,
    NonNegativeInt,
    PositiveFloat,
)

from app.domain.entities import DomainEntity
from app.domain.stores.entities import StoreSlug

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
    margin_amount: NonNegativeFloat
    margin_rate: NonNegativeFloat


class ArticleStoreData(BaseModel):
    gross_price: PositiveFloat
    bar_price: NonNegativeFloat
    stock_quantity: int
    recommended_price: PositiveFloat
    margins: ArticleMargins


class BaseArticle(BaseModel):
    category: str
    name: ArticleName
    cost_price: PositiveFloat
    excise_duty: NonNegativeFloat = 0.0
    social_security_contribution: NonNegativeFloat = 0.0
    vat_rate: float
    distributor: str
    barcode: str = ""
    region: str = ""
    color: ArticleColor = ArticleColor.UNDEFINED
    taste: ArticleTaste = ArticleTaste.UNDEFINED
    volume: ArticleVolume | None
    alcohol_by_volume: NonNegativeFloat = 0.0
    packaging: NonNegativeInt = 0
    deposit: ArticleDeposit

    @property
    def total_cost(self) -> float:
        total_cost_sum = sum(
            [self.cost_price, self.excise_duty, self.social_security_contribution]
        )
        return round(total_cost_sum, 4)

    def inventory_value(self, stock_quantity: int) -> float:
        return round((self.total_cost * stock_quantity), 2)

    def deposit_value(self, stock_quantity: int) -> float:
        if self.deposit.unit == 0:
            return 0

        if self.packaging > 0:
            value = self.deposit.case * (stock_quantity / self.packaging)
            return round(value, 2)

        return self.deposit.unit * stock_quantity

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
    store_data: dict[StoreSlug, ArticleStoreData]


class Article(DomainEntity, BaseArticle):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    store_data: dict[StoreSlug, ArticleStoreData]
