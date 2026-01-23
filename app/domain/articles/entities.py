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


class ColorCategory(StrEnum):
    BEER = "beer"
    WINE = "wine"


class CategorizedStrEnum(StrEnum):
    _category: ColorCategory

    def __new__(cls, value: str, category: ColorCategory) -> CategorizedStrEnum:
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj._category = category
        return obj

    @property
    def category(self) -> ColorCategory:
        return self._category

    @classmethod
    def from_category[T: CategorizedStrEnum](
        cls: type[T], category: ColorCategory, /
    ) -> list[T]:
        return [item for item in cls if item.category == category]


class ArticleColor(CategorizedStrEnum):
    AMBER_BEER = ("Ambrée", ColorCategory.BEER)
    WHITE_BEER = ("Blanche", ColorCategory.BEER)
    BLONDE_BEER = ("Blonde", ColorCategory.BEER)
    BROWN_BEER = ("Brune", ColorCategory.BEER)
    FRUITY_BEER = ("Fruitée", ColorCategory.BEER)
    WHITE_WINE = ("Blanc", ColorCategory.WINE)
    ROSE_WINE = ("Rosé", ColorCategory.WINE)
    RED_WINE = ("Rouge", ColorCategory.WINE)


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
    unit: Annotated[DecimalType, Field(gt=0, decimal_places=2)]
    case: Annotated[DecimalType | None, Field(gt=0, decimal_places=2)]
    packaging: PositiveInt | None


class ArticleMargins(BaseModel):
    margin_amount: Annotated[DecimalType, Field(decimal_places=2)]
    margin_rate: Annotated[DecimalType, Field(decimal_places=0)]


class ArticleStoreData(BaseModel):
    gross_price: Annotated[DecimalType, Field(gt=0, decimal_places=2)]
    bar_price: Annotated[DecimalType, Field(ge=0, decimal_places=2)]
    stock_quantity: int  # can be negative (handle by POS)
    recommended_price: Annotated[DecimalType, Field(gt=0, decimal_places=2)]
    margins: ArticleMargins


class BaseArticle(BaseModel):
    category: str
    producer: Annotated[str | None, Field(min_length=1, default=None)]
    product: str
    cost_price: Annotated[DecimalType, Field(gt=0, decimal_places=4)]
    excise_duty: Annotated[
        DecimalType,
        Field(ge=0, decimal_places=4, default=Decimal(0)),
    ]
    social_security_contribution: Annotated[
        DecimalType,
        Field(ge=0, decimal_places=4, default=Decimal(0)),
    ]
    vat_rate: Annotated[DecimalType, Field(ge=0, le=100, decimal_places=2)]
    distributor: str
    barcode: str = ""
    origin: Annotated[str | None, Field(min_length=1)]
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

    def deposit_value(self, stock_quantity: int) -> Decimal | None:
        if not self.deposit:
            return None

        if self.deposit.case and self.deposit.packaging:
            return self.deposit.case * (
                Decimal(stock_quantity) / Decimal(self.deposit.packaging)
            )

        return self.deposit.unit * Decimal(stock_quantity)


class ArticleCreateOrUpdate(BaseArticle):
    store_data: dict[StoreSlug, ArticleStoreData]


class Article(DomainEntity, BaseArticle):
    reference: Annotated[uuid.UUID, PlainSerializer(str)]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    store_data: dict[StoreSlug, ArticleStoreData]
