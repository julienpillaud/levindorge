from pydantic import (
    BaseModel,
    NonNegativeInt,
    PositiveInt,
)

from app.domain.types import EntityId

DEFAULT_PAGINATION_SIZE = 100


class DomainEntity(BaseModel):
    id: EntityId = ""


class PaginatedResponse[T: DomainEntity](BaseModel):
    page: PositiveInt
    limit: NonNegativeInt
    total: NonNegativeInt
    total_pages: NonNegativeInt
    items: list[T]
