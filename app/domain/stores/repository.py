from typing import Protocol

from cleanstack.domain import RepositoryProtocol

from app.domain.stores.entities import Store
from app.domain.types import StoreSlug


class StoreRepositoryProtocol(RepositoryProtocol[Store], Protocol):
    def create_many(self, stores: list[Store]) -> list[Store]: ...

    def get_by_slug(self, slug: StoreSlug) -> Store | None: ...
