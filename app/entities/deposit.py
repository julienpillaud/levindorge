from typing import Literal

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class RequestDeposit(BaseModel):
    category: Literal["Bière", "Fût", "Mini-fût"]
    deposit_type: Literal["Unitaire", "Caisse"]
    value: float


class Deposit(RequestDeposit):
    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    def convert_objectid(cls, value: ObjectId) -> str:
        if not ObjectId.is_valid(value):
            raise ValueError("Must be an ObjectId")
        return str(value)
