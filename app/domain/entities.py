from pydantic import (
    BaseModel,
    NonNegativeInt,
    PositiveInt,
)

type EntityId = str

DEFAULT_PAGINATION_SIZE = 100


class DomainEntity(BaseModel):
    id: EntityId = ""


class PaginatedResponse[T: DomainEntity](BaseModel):
    page: PositiveInt
    limit: NonNegativeInt
    total: NonNegativeInt
    total_pages: NonNegativeInt
    items: list[T]
