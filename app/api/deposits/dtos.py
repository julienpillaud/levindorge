from typing import Annotated

from pydantic import BaseModel, Field

from app.domain.deposits.entities import DepositCategory, DepositType
from app.domain.types import DecimalType


class DepositDTO(BaseModel):
    value: Annotated[DecimalType, Field(gt=0, decimal_places=2)]
    type: DepositType
    category: DepositCategory
