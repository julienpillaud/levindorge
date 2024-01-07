from bson import ObjectId
from pydantic import Field, field_validator

from app.entities.article import ArticleVolume


class RequestVolume(ArticleVolume):
    category: str


class Volume(RequestVolume):
    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    def convert_objectid(cls, value: ObjectId) -> str:
        if not ObjectId.is_valid(value):
            raise ValueError("Must be an ObjectId")
        return str(value)
