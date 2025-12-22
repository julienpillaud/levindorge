from app.domain.categories.commands import (
    get_categories_command,
    get_category_by_name_command,
)
from app.domain.commons.category_groups import CategoryGroupName
from app.domain.context import ContextProtocol
from tests.factories.categories import CategoryFactory


def test_get_categories(
    context: ContextProtocol,
    category_factory: CategoryFactory,
) -> None:
    categories_count = 3
    category_factory.create_many(categories_count)

    result = get_categories_command(context)

    assert result.total == categories_count
    categories = result.items
    assert len(categories) == categories_count


def test_get_categories_by_category_group(
    context: ContextProtocol,
    category_factory: CategoryFactory,
) -> None:
    categories_count = 3
    category_factory.create_many(
        categories_count,
        category_group=CategoryGroupName.SPIRIT,
    )
    category_factory.create_one(category_group=CategoryGroupName.BEER)

    result = get_categories_command(context, category_group=CategoryGroupName.BEER)

    assert result.total == 1
    categories = result.items
    assert len(categories) == 1


def test_get_category_by_name(
    context: ContextProtocol,
    category_factory: CategoryFactory,
) -> None:
    category = category_factory.create_one()

    result = get_category_by_name_command(context, category.name)

    assert result.name == category.name
