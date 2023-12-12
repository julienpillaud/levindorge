from typing import Literal

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class RequestVolume(BaseModel):
    category: str
    unit: Literal["cL", "L"]
    value: float


class Volume(RequestVolume):
    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    def convert_objectid(cls, value: ObjectId) -> str:
        if not ObjectId.is_valid(value):
            raise ValueError("Must be an ObjectId")
        return str(value)
