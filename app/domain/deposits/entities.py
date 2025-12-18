from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, Field

from app.domain.entities import DomainEntity
from app.domain.types import DecimalType


class DepositType(StrEnum):
    UNIT = "unit"
    CASE = "case"


class DepositCategory(StrEnum):
    BEER = "beer"
    KEG = "keg"


class Deposit(DomainEntity):
    value: Annotated[DecimalType, Field(gt=0, decimal_places=2)]
    type: DepositType
    category: DepositCategory


class DepositCreate(BaseModel):
    value: float
    type: DepositType
    category: DepositCategory
