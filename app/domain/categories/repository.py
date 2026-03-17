from typing import Protocol

from cleanstack.domain import RepositoryProtocol

from app.domain.categories.entities import Category


class CategoryRepositoryProtocol(RepositoryProtocol[Category], Protocol):
    def create_many(self, categories: list[Category]) -> list[Category]: ...

    def get_by_name(self, name: str) -> Category | None: ...
