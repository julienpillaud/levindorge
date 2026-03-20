import datetime
import uuid
from decimal import Decimal
from typing import Annotated

from cleanstack.entities import DomainEntity
from pydantic import BaseModel, Field, NonNegativeFloat

from app.domain.metadata.entities.deposits import ArticleDeposit
from app.domain.metadata.entities.origins import ArticleOrigin
from app.domain.metadata.entities.volumes import ArticleVolume
from app.domain.types import DecimalType, StoreSlug


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
    producer: str | None
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
    barcode: str
    origin: ArticleOrigin | None
    color: str | None
    taste: str | None
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
    reference: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    store_data: dict[StoreSlug, ArticleStoreData]
