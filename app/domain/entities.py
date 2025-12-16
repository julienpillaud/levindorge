from typing import Any

from pydantic import (
    BaseModel,
    NonNegativeInt,
    PositiveInt,
)

from app.domain.types import EntityId

DEFAULT_PAGINATION_SIZE = 100


class DomainEntity(BaseModel):
    id: EntityId = ""

    # Temporary until refactoring is complete
    @classmethod
    def to_domain_entity[T: DomainEntity](
        cls: type[T],
        document: dict[str, Any],
        /,
    ) -> T:
        document["id"] = str(document.pop("_id"))
        return cls.model_validate(document)


class PaginatedResponse[T: DomainEntity](BaseModel):
    page: PositiveInt
    limit: NonNegativeInt
    total: NonNegativeInt
    total_pages: NonNegativeInt
    items: list[T]
