from cleanstack.exceptions import NotFoundError

from app.domain.categories.entities import Category
from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse


def get_categories_command(context: ContextProtocol) -> PaginatedResponse[Category]:
    return context.category_repository.get_all()


def get_category_by_name_command(context: ContextProtocol, name: str) -> Category:
    category = context.category_repository.get_by_name(name=name)
    if not category:
        raise NotFoundError()

    return category
