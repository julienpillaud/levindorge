from datetime import datetime

from pydantic import BaseModel, field_validator

type_mapping = {"biere-vin": "Bière / Vin", "spirit": "Spiritueux"}
shop_mapping = {
    "angouleme": "Angoulême",
    "sainte-eulalie": "Sainte-Eulalie",
    "pessac": "Pessac",
}


class TagFile(BaseModel):
    id: str
    type: str
    shop: str
    date: datetime
    file: str

    @field_validator("type")
    @classmethod
    def convert_type(cls, value: str) -> str:
        return type_mapping.get(value, "")

    @field_validator("shop")
    @classmethod
    def convert_shop(cls, value: str) -> str:
        return shop_mapping.get(value, "")
