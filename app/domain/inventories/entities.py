import datetime
from decimal import Decimal

from pydantic import BaseModel, PositiveFloat, field_serializer

from app.domain.articles.entities import ArticleDeposit
from app.domain.entities import DomainEntity
from app.domain.types import EntityId


class InventoryRecord(BaseModel):
    inventory_id: EntityId
    article_id: EntityId
    article_name: str
    article_volume: float = 0.0
    article_deposit: ArticleDeposit
    article_type: str
    taxfree_price: PositiveFloat
    stock_quantity: int
    sale_value: float
    deposit_value: float = 0.0


class InventoryDetail(BaseModel):
    sale_value: Decimal = Decimal("0.0")
    deposit_value: Decimal = Decimal("0.0")

    def add(self, inventory_value: float, deposit_value: float) -> None:
        self.sale_value += Decimal(str(inventory_value))
        self.deposit_value += Decimal(str(deposit_value))

    @field_serializer("sale_value", "deposit_value")
    def decimal_to_float(self, value: Decimal) -> float:
        return float(value.quantize(Decimal("0.01")))


class Inventory(DomainEntity):
    date: datetime.datetime
    shop: str
    inventory: dict[str, InventoryDetail]
    sale_value: float = 0
    deposit_value: float = 0


class InventoryReport(Inventory):
    records: list[InventoryRecord]
