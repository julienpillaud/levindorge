from enum import StrEnum
from typing import Annotated

from cleanstack.entities import DomainEntity
from pydantic import BaseModel, Field, PositiveInt

from app.domain.types import DecimalType

DepositValue = Annotated[DecimalType, Field(gt=0, decimal_places=2)]


class DepositType(StrEnum):
    UNIT = "unit"
    CASE = "case"


class Deposit(DomainEntity):
    value: DepositValue
    type: DepositType


class ArticleDeposit(BaseModel):
    unit: DepositValue
    case: DepositValue | None
    packaging: PositiveInt | None
