from pydantic import (
    BaseModel,
    NonNegativeInt,
    PositiveInt,
)

from app.domain.filters import FilterEntity

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


class QueryParams(BaseModel):
    filters: list[FilterEntity] | None = None
    search: str | None = None
    sort: dict[str, int] | None = None
