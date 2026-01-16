import random
from typing import Any

from app.domain.categories.entities import Category
from app.infrastructure.repository.categories import CategoryRepository
from scripts.migration.categories import CATEGORIES
from tests.factories.base import BaseMongoFactory


def generate_category(**kwargs: Any) -> Category:
    filtered = CATEGORIES
    for key, value in kwargs.items():
        filtered = [
            category for category in filtered if getattr(category, key, None) == value
        ]
    return random.choice(filtered)


class CategoryFactory(BaseMongoFactory[Category]):
    repository_class = CategoryRepository

    def build(self, **kwargs: Any) -> Category:
        return generate_category(**kwargs)
