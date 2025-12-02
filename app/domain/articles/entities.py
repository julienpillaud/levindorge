import datetime
import uuid
from decimal import Decimal
from enum import StrEnum
from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    NonNegativeFloat,
    PlainSerializer,
    PositiveFloat,
    PositiveInt,
)

from app.domain.entities import DomainEntity
from app.domain.types import DecimalType, StoreSlug
from app.domain.volumes.entities import VolumeUnit

LITER_TO_CENTILITER = 100


class ArticleColor(StrEnum):
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
    unit: VolumeUnit

    def __str__(self) -> str:
        formatted_value = str(self.value).rstrip("0").rstrip(".").replace(".", ",")
        return f"{formatted_value} {self.unit}"


class ArticleDeposit(BaseModel):
    unit: PositiveFloat
    case: PositiveFloat | None
    packaging: PositiveInt | None


class ArticleMargins(BaseModel):
    margin_amount: DecimalType = Field(decimal_places=2)
    margin_rate: DecimalType = Field(decimal_places=0)


class ArticleStoreData(BaseModel):
    gross_price: DecimalType = Field(gt=0, decimal_places=2)
    bar_price: DecimalType = Field(ge=0, decimal_places=2)
    stock_quantity: int
    recommended_price: DecimalType = Field(gt=0, decimal_places=2)
    margins: ArticleMargins


class BaseArticle(BaseModel):
    reference: Annotated[uuid.UUID, PlainSerializer(str)] = Field(
        default_factory=uuid.uuid7
    )
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
    origin: str | None
    color: ArticleColor | None
    taste: ArticleTaste | None
    volume: ArticleVolume | None
    alcohol_by_volume: NonNegativeFloat | None
    deposit: ArticleDeposit | None

    @property
    def display_name(self) -> str:
        name = self.product
        if self.producer:
            name = f"{self.producer} {name}"
        if self.volume:
            name = f"{name} {self.volume}"
        return name

    @property
    def total_cost(self) -> Decimal:
        return self.cost_price + self.excise_duty + self.social_security_contribution

    def inventory_value(self, stock_quantity: int) -> Decimal:
        return self.total_cost * stock_quantity

    def deposit_value(self, stock_quantity: int) -> float | None:
        if not self.deposit:
            return None

        if self.deposit.case and self.deposit.packaging:
            value = self.deposit.case * (stock_quantity / self.deposit.packaging)
            return round(value, 2)

        return self.deposit.unit * stock_quantity


class ArticleCreateOrUpdate(BaseArticle):
    store_data: dict[StoreSlug, ArticleStoreData]


class Article(DomainEntity, BaseArticle):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    store_data: dict[StoreSlug, ArticleStoreData]
