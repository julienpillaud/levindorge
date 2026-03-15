from enum import StrEnum

from pydantic import (
    BaseModel,
    NonNegativeInt,
    PositiveInt,
)

type EntityId = str

DEFAULT_PAGINATION_SIZE = 100


class DomainEntity(BaseModel):
    id: EntityId = ""


class Pagination(BaseModel):
    page: PositiveInt = 1
    limit: PositiveInt = DEFAULT_PAGINATION_SIZE

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.limit


class PaginatedResponse[T: DomainEntity](BaseModel):
    page: PositiveInt
    limit: NonNegativeInt
    total: NonNegativeInt
    total_pages: NonNegativeInt
    items: list[T]


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


class SortEntity(BaseModel):
    field: str
    order: SortOrder = SortOrder.ASC
