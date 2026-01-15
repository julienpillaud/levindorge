from enum import StrEnum

from pydantic import BaseModel


class FilterOperator(StrEnum):
    EQ = "eq"


class FilterEntity(BaseModel):
    field: str
    value: str | list[str]
    operator: FilterOperator = FilterOperator.EQ
