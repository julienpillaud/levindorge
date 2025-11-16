from app.core.core import Context
from app.domain.categories.entities import Category


def update_categories(src_context: Context, dst_context: Context) -> None:
    src_categories = src_context.database["types"].find()
    dst_categories = [
        Category(
            name=category["name"],
            pricing_group=category["ratio_category"],
            tactill_category=category["tactill_category"],
        )
        for category in src_categories
    ]

    dst_context.category_repository.create_many(dst_categories)
