from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, Field

from app.domain.entities import DomainEntity
from app.domain.types import DecimalType


class DepositType(StrEnum):
    UNIT = "unit"
    CASE = "case"

    @property
    def label(self) -> str:
        mapping = {DepositType.UNIT: "Unitaire", DepositType.CASE: "Caisse"}
        return mapping[self]


class DepositCategory(StrEnum):
    BEER = "beer"
    KEG = "keg"

    @property
    def label(self) -> str:
        mapping = {DepositCategory.BEER: "Bière", DepositCategory.KEG: "Fût"}
        return mapping[self]


class Deposit(DomainEntity):
    value: Annotated[DecimalType, Field(gt=0, decimal_places=2)]
    type: DepositType
    category: DepositCategory

    @property
    def display_name(self) -> str:
        return f'"{self.value} {self.type.label} {self.category.label}"'


class DepositCreate(BaseModel):
    value: Annotated[DecimalType, Field(gt=0, decimal_places=2)]
    type: DepositType
    category: DepositCategory
