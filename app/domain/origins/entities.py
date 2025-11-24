from enum import StrEnum
from typing import Literal

from app.domain.entities import DomainEntity


class OriginType(StrEnum):
    COUNTRY = "country"
    REGION = "region"


class Origin(DomainEntity):
    name: str
    code: str | None
    type: OriginType


class Country(Origin):
    name: str
    code: str
    type: Literal[OriginType.COUNTRY] = OriginType.COUNTRY


class Region(Origin):
    name: str
    code: None = None
    type: Literal[OriginType.REGION] = OriginType.REGION
