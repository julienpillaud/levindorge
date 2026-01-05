from cleanstack.exceptions import NotFoundError

from app.domain.caching import cached_command
from app.domain.categories.entities import Category
from app.domain.commons.category_groups import CategoryGroupName
from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse


@cached_command(response_model=PaginatedResponse[Category], tag="categories")
def get_categories_command(
    context: ContextProtocol,
    /,
    category_group: CategoryGroupName | None = None,
) -> PaginatedResponse[Category]:
    filters = {"category_group": category_group} if category_group else {}
    return context.category_repository.get_all(
        filters=filters,
        sort={"name": 1},
        limit=300,
    )


def get_category_by_name_command(context: ContextProtocol, /, name: str) -> Category:
    category = context.category_repository.get_by_name(name=name)
    if not category:
        raise NotFoundError(f"Category '{name}' not found.")

    return category
