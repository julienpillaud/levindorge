from enum import StrEnum
from typing import Literal

from pydantic import BaseModel

from app.domain.entities import DomainEntity


class OriginType(StrEnum):
    COUNTRY = "country"
    REGION = "region"


class Origin(DomainEntity):
    name: str
    code: str | None
    type: OriginType

    @property
    def display_name(self) -> str:
        return self.name


class Country(Origin):
    name: str
    code: str
    type: Literal[OriginType.COUNTRY] = OriginType.COUNTRY


class Region(Origin):
    name: str
    code: None = None
    type: Literal[OriginType.REGION] = OriginType.REGION


class OriginCreate(BaseModel):
    name: str
    code: str | None
    type: OriginType
