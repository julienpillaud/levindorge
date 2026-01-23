from enum import StrEnum
from typing import Self

from pydantic import BaseModel, model_validator

from app.domain.entities import DomainEntity


class OriginType(StrEnum):
    COUNTRY = "country"
    REGION = "region"


class Origin(DomainEntity):
    name: str
    code: str | None = None
    type: OriginType = OriginType.COUNTRY

    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.type == OriginType.COUNTRY and not self.code:
            raise ValueError("Country must have a code")
        return self

    @property
    def display_name(self) -> str:
        return self.name


class OriginCreate(BaseModel):
    name: str
    code: str | None
    type: OriginType
