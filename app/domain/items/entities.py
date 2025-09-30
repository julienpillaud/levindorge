from enum import StrEnum
from typing import Literal

from app.domain.entities import DomainModel


class ItemName(StrEnum):
    BREWERIES = "breweries"
    DISTILLERIES = "distilleries"
    DISTRIBUTORS = "distributors"
    COUNTRIES = "countries"
    REGIONS = "regions"
    VOLUMES = "volumes"
    DEPOSITS = "deposits"


class Item(DomainModel):
    name: str
    demonym: str = ""


class Volume(DomainModel):
    value: float
    unit: Literal["cL", "L"]
    category: str


class Deposit(DomainModel):
    category: Literal["Bière", "Fût", "Mini-fût"]
    deposit_type: Literal["Unitaire", "Caisse"]
    value: float
