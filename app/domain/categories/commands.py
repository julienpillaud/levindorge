from cleanstack.domain import NotFoundError
from cleanstack.entities import (
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
    SortOrder,
)

from app.domain.caching import cached_command
from app.domain.categories.entities import Category
from app.domain.commons.category_groups import CategoryGroupName
from app.domain.context import ContextProtocol


@cached_command(return_type=PaginatedResponse[Category], tag="categories")
def get_categories_command(
    context: ContextProtocol,
    /,
    category_group: CategoryGroupName | None = None,
) -> PaginatedResponse[Category]:
    filters = (
        [FilterEntity(field="category_group", value=category_group)]
        if category_group
        else []
    )

    return context.category_repository.get_all(
        filters=filters,
        sort=[SortEntity(field="name", order=SortOrder.ASC)],
        pagination=Pagination(page=1, size=300),
    )


@cached_command(return_type=Category, tag="category")
def get_category_by_name_command(context: ContextProtocol, /, name: str) -> Category:
    category = context.category_repository.get_by_name(name=name)
    if not category:
        raise NotFoundError(f"Category '{name}' not found.")

    return category
