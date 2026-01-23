from rich import print

from app.core.core import Context
from app.domain.categories.entities import Category
from app.domain.entities import Pagination
from data.categories import CATEGORIES


def create_categories(dst_context: Context) -> list[Category]:
    result = dst_context.category_repository.create_many(CATEGORIES)
    count = len(result)
    print(f"Created {count} categories")
    return dst_context.category_repository.get_all(
        pagination=Pagination(
            page=1,
            limit=count,
        )
    ).items
