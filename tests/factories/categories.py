from typing import Any

from polyfactory.factories.pydantic_factory import ModelFactory

from app.domain.categories.entities import Category
from app.infrastructure.repository.categories import CategoryRepository
from tests.factories.base import BaseMongoFactory


class CategoryEntityFactory(ModelFactory[Category]): ...


class CategoryFactory(BaseMongoFactory[Category]):
    repository_class = CategoryRepository

    def build(self, **kwargs: Any) -> Category:
        return CategoryEntityFactory.build(**kwargs)
