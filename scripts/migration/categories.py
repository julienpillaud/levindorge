from cleanstack.entities import Pagination
from rich import print

from app.core.context import Context
from app.domain.categories.entities import Category
from data.categories import CATEGORIES


def create_categories(dst_context: Context) -> list[Category]:
    result = dst_context.category_repository.create_many(CATEGORIES)

    count = len(result)
    print(f"Created {count} categories")

    return dst_context.category_repository.get_all(
        pagination=Pagination(page=1, size=count)
    ).items
