from enum import StrEnum
from typing import Literal

from app.domain.entities import DomainModel


class ItemType(StrEnum):
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

    @property
    def name(self) -> str:
        return f"Volume {self.value:g} {self.unit}"


class Deposit(DomainModel):
    category: Literal["Bière", "Fût", "Mini-fût"]
    deposit_type: Literal["Unitaire", "Caisse"]
    value: float

    @property
    def name(self) -> str:
        return f"Consigne {self.category} {self.value:g} {self.deposit_type}"
