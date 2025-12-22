from typing import Any, Protocol

from pydantic import PositiveInt

from app.domain.entities import (
    DEFAULT_PAGINATION_SIZE,
    DomainEntity,
    EntityId,
    PaginatedResponse,
)


class RepositoryProtocol[T: DomainEntity](Protocol):
    def get_all(
        self,
        filters: Any | None = None,
        search: str | None = None,
        sort: Any | None = None,
        page: PositiveInt = 1,
        limit: PositiveInt = DEFAULT_PAGINATION_SIZE,
    ) -> PaginatedResponse[T]: ...

    def get_by_id(self, entity_id: str, /) -> T | None: ...

    def create(self, entity: T, /) -> T: ...

    def create_many(self, entities: list[T], /) -> list[EntityId]: ...

    def update(self, entity: T, /) -> T: ...

    def delete(self, entity: T, /) -> None: ...
