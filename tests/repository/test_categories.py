from app.infrastructure.repository.categories import CategoryRepository
from tests.factories.categories import CategoryFactory
from tests.utils import is_str_object_id


def test_create_category(
    category_factory: CategoryFactory,
    category_repository: CategoryRepository,
) -> None:
    category = category_factory.build()

    category_db = category_repository.create(category)

    assert is_str_object_id(category_db.id)
    assert category_db.name == category.name
    assert category_db.pricing_group == category.pricing_group
    assert category_db.tactill_category == category.tactill_category


def test_get_categories(
    category_factory: CategoryFactory,
    category_repository: CategoryRepository,
) -> None:
    items_count = 4
    limit = 3
    category_factory.create_many(items_count)

    result = category_repository.get_all(limit=limit)

    assert result.page == 1
    assert result.limit == limit
    assert result.total == items_count
    assert result.total_pages == (items_count + limit - 1) // limit
    assert len(result.items) == limit


def test_get_category(
    category_factory: CategoryFactory,
    category_repository: CategoryRepository,
) -> None:
    categories = category_factory.create_many(3)

    category = categories[0]
    category_db = category_repository.get_by_id(category.id)

    assert category_db
    assert is_str_object_id(category_db.id)
    assert category_db.name == category.name
    assert category_db.pricing_group == category.pricing_group
    assert category_db.tactill_category == category.tactill_category
