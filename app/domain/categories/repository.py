from typing import Protocol

from app.domain._shared.protocols.repository import RepositoryProtocol
from app.domain.categories.entities import Category


class CategoryRepositoryProtocol(RepositoryProtocol[Category], Protocol):
    def get_by_name(self, name: str) -> Category | None: ...
