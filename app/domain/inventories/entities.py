import datetime
from decimal import Decimal
from typing import Annotated

from cleanstack.entities import DomainEntity, EntityId
from pydantic import BaseModel, Field, field_validator

from app.domain.commons.entities import InventoryGroup
from app.domain.types import DecimalType, StoreName


class InventoryRecord(DomainEntity):
    inventory_id: EntityId
    article_id: EntityId | None  # Can be None for legacy
    article_name: str | None  # As id fallback for legacy
    stock_quantity: int
    inventory_value: Annotated[DecimalType, Field(ge=0, decimal_places=2)]
    deposit_value: Annotated[DecimalType | None, Field(ge=0, decimal_places=2)]


class InventoryDetail(BaseModel):
    inventory_value: Annotated[DecimalType, Field(ge=0, decimal_places=2)]
    deposit_value: Annotated[DecimalType | None, Field(ge=0, decimal_places=2)]

    def add(self, inventory_value: Decimal, deposit_value: Decimal | None) -> None:
        self.inventory_value += inventory_value
        if self.deposit_value and deposit_value:
            self.deposit_value += deposit_value

    #
    # @field_serializer("sale_value", "deposit_value")
    # def decimal_to_float(self, value: Decimal) -> float:
    #     return float(value.quantize(Decimal("0.01")))


class Inventory(DomainEntity):
    created_at: datetime.datetime
    store: StoreName
    inventory: dict[InventoryGroup, InventoryDetail]
    inventory_value: Annotated[DecimalType, Field(ge=0, decimal_places=2)]
    deposit_value: Annotated[DecimalType | None, Field(ge=0, decimal_places=2)]

    @field_validator("inventory", mode="after")
    @classmethod
    def sort_inventory(
        cls,
        value: dict[InventoryGroup, InventoryDetail],
    ) -> dict[InventoryGroup, InventoryDetail]:
        return {group: value[group] for group in InventoryGroup if group in value}
