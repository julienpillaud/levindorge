from enum import StrEnum

from pydantic import BaseModel

from app.domain.entities import DomainModel


class ItemType(StrEnum):
    BREWERIES = "breweries"
    DISTILLERIES = "distilleries"
    DISTRIBUTORS = "distributors"
    COUNTRIES = "countries"
    REGIONS = "regions"
    VOLUMES = "volumes"
    DEPOSITS = "deposits"


class ItemCreate(BaseModel):
    name: str
    demonym: str = ""


class Item(DomainModel):
    name: str
    demonym: str = ""
