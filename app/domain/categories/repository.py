from typing import Protocol

from app.domain.categories.entities import Category
from app.domain.protocols.repository import RepositoryProtocol


class CategoryRepositoryProtocol(RepositoryProtocol[Category], Protocol):
    def get_by_name(self, name: str) -> Category | None: ...
