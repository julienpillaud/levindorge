import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    NonNegativeFloat,
    NonNegativeInt,
    PositiveFloat,
)

from app.domain.entities import DecimalType, DomainEntity
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


class ArticleVolume(BaseModel):
    value: PositiveFloat
    unit: Literal["cL", "L"]


class ArticleDeposit(BaseModel):
    unit: NonNegativeFloat
    case: NonNegativeFloat


class ArticleMargins(BaseModel):
    margin_amount: DecimalType = Field(ge=0, decimal_places=2)
    margin_rate: DecimalType = Field(ge=0, le=100, decimal_places=0)


class ArticleStoreData(BaseModel):
    gross_price: DecimalType = Field(gt=0, decimal_places=2)
    bar_price: DecimalType = Field(ge=0, decimal_places=2)
    stock_quantity: int
    recommended_price: DecimalType = Field(gt=0, decimal_places=2)
    margins: ArticleMargins


class BaseArticle(BaseModel):
    category: str
    producer: str | None = Field(min_length=1, default=None)
    product: str
    cost_price: DecimalType = Field(gt=0, decimal_places=4)
    excise_duty: DecimalType = Field(ge=0, decimal_places=4, default=Decimal(0))
    social_security_contribution: DecimalType = Field(
        ge=0, decimal_places=4, default=Decimal(0)
    )
    vat_rate: DecimalType = Field(ge=0, le=100, decimal_places=2)
    distributor: str
    barcode: str = ""
    origin: str | None = None
    color: ArticleColor = ArticleColor.UNDEFINED
    taste: ArticleTaste = ArticleTaste.UNDEFINED
    volume: ArticleVolume | None
    alcohol_by_volume: NonNegativeFloat = 0.0
    packaging: NonNegativeInt = 0
    deposit: ArticleDeposit

    @property
    def display_name(self) -> str:
        name = self.product
        if self.producer:
            name = f"{self.producer} {name}"
        if self.volume:
            name = f"{name} {self.formated_volume(separator=',')}"
        return name

    @property
    def total_cost(self) -> Decimal:
        return self.cost_price + self.excise_duty + self.social_security_contribution

    def inventory_value(self, stock_quantity: int) -> Decimal:
        return self.total_cost * stock_quantity

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
        return f"{formatted_value} {unit}"


class ArticleCreateOrUpdate(BaseArticle):
    store_data: dict[StoreSlug, ArticleStoreData]


class Article(DomainEntity, BaseArticle):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    store_data: dict[StoreSlug, ArticleStoreData]
