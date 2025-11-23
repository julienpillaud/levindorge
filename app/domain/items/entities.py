from enum import StrEnum

from pydantic import BaseModel

from app.domain.entities import DomainEntity


class ItemType(StrEnum):
    DISTRIBUTORS = "distributors"
    COUNTRIES = "countries"
    REGIONS = "regions"
    VOLUMES = "volumes"
    DEPOSITS = "deposits"


class ItemCreate(BaseModel):
    name: str
    demonym: str = ""


class Item(DomainEntity):
    name: str
    demonym: str = ""
