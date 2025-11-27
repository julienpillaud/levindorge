from enum import StrEnum

from pydantic import BaseModel

from app.domain.entities import DomainEntity


class DepositType(StrEnum):
    UNIT = "unit"
    CASE = "case"


class DepositCategory(StrEnum):
    BEER = "beer"
    KEG = "keg"
    MINI_KEG = "mini_keg"


class Deposit(DomainEntity):
    value: float
    type: DepositType
    category: DepositCategory


class DepositCreate(BaseModel):
    value: float
    type: DepositType
    category: DepositCategory
