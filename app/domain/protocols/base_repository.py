from typing import Any, Protocol

from app.domain.entities import DomainModel, PaginatedResponse, Pagination


class RepositoryProtocol[T: DomainModel](Protocol):
    def get_all(
        self,
        filters: dict[str, Any] | None = None,
        search: str | None = None,
        sort: dict[str, int] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[T]: ...

    def get_by_id(self, entity_id: str, /) -> T | None: ...

    def create(self, entity: T, /) -> T: ...

    def update(self, entity: T, /) -> T: ...

    def delete(self, entity: T, /) -> None: ...
