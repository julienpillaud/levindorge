from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator


class RequestInventory(BaseModel):
    article_id: str
    stock_quantity: int


class CreateOrUpdateInventory(RequestInventory):
    sale_value: float
    deposit_value: float


class Inventory(CreateOrUpdateInventory):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    def convert_objectid(cls, value: ObjectId) -> str:
        if not ObjectId.is_valid(value):
            raise ValueError("Must be an ObjectId")
        return str(value)
