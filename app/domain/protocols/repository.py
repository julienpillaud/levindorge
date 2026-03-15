from typing import Protocol

from app.domain.entities import (
    DomainEntity,
    EntityId,
    PaginatedResponse,
    Pagination,
    SortEntity,
)
from app.domain.filters import FilterEntity


class RepositoryProtocol[T: DomainEntity](Protocol):
    def get_all(
        self,
        filters: list[FilterEntity] | None = None,
        search: str | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[T]: ...

    def get_by_id(self, entity_id: EntityId, /) -> T | None: ...

    def create(self, entity: T, /) -> T: ...

    def create_many(self, entities: list[T], /) -> list[EntityId]: ...

    def update(self, entity: T, /) -> T: ...

    def delete(self, entity: T, /) -> None: ...
