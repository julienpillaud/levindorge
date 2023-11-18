from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator

from application.entities.article import ArticleDeposit, ArticleName


class RequestResetStocks(BaseModel):
    shop: str
    category: str


class InventoryDetail(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    sale_value: float = 0
    deposit_value: float = 0

    @field_validator("*")
    def round(cls, value: float) -> float:
        return round(value, 2)


class InventoryValues(RootModel[dict[str, InventoryDetail]]):
    root: dict[str, InventoryDetail]

    def __getitem__(self, item: str) -> InventoryDetail:
        return self.root[item]

    def get(self, *args, **kwargs):
        return self.root.get(*args, **kwargs)

    def items(self):
        return self.root.items()


class CreateInventory(BaseModel):
    date: datetime
    shop: str
    inventory: InventoryValues | None = None
    sale_value: float = 0
    deposit_value: float = 0


class UpdateInventory(BaseModel):
    inventory: InventoryValues
    sale_value: float
    deposit_value: float

    @field_validator("sale_value", "deposit_value")
    def round(cls, value: float) -> float:
        return round(value, 2)


class Inventory(CreateInventory):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    def convert_objectid(cls, value: ObjectId) -> str:
        if not ObjectId.is_valid(value):
            raise ValueError("Must be an ObjectId")
        return str(value)


class CreateInventoryRecord(BaseModel):
    inventory_id: str
    article_id: str
    article_name: ArticleName
    article_volume: float = 0.0
    article_packaging: int = 0
    article_deposit: ArticleDeposit
    article_type: str
    taxfree_price: float
    stock_quantity: int
    sale_value: float
    deposit_value: float = 0.0

    @field_validator("sale_value", "deposit_value")
    def round(cls, value: float) -> float:
        return round(value, 2)


class InventoryRecord(CreateInventoryRecord):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    def convert_objectid(cls, value: ObjectId) -> str:
        if not ObjectId.is_valid(value):
            raise ValueError("Must be an ObjectId")
        return str(value)
