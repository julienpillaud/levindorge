from cleanstack.exceptions import NotFoundError

from app.domain.categories.entities import Category
from app.domain.context import ContextProtocol


def get_category_by_name_command(context: ContextProtocol, name: str) -> Category:
    category = context.category_repository.get_by_name(name=name)
    if not category:
        raise NotFoundError()

    return category
