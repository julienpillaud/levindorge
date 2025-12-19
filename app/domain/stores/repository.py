from typing import Protocol

from app.domain._shared.protocols.repository import RepositoryProtocol
from app.domain.stores.entities import Store
from app.domain.types import StoreSlug


class StoreRepositoryProtocol(RepositoryProtocol[Store], Protocol):
    def get_by_slug(self, slug: StoreSlug) -> Store | None: ...
