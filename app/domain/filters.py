from enum import StrEnum

from pydantic import BaseModel


class FilterOperator(StrEnum):
    EQ = "eq"
    IN = "in"


class FilterEntity(BaseModel):
    field: str
    value: str | list[str]
    operator: FilterOperator = FilterOperator.EQ
