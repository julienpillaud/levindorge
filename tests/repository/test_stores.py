from app.infrastructure.repository.stores import StoreRepository
from tests.factories.stores import StoreFactory


def test_create_store(
    store_factory: StoreFactory,
    store_repository: StoreRepository,
) -> None:
    store = store_factory.build_entity()

    store_db = store_repository.create(store)

    assert store_db.name == store.name
    assert store_db.slug == store.slug
    assert store_db.tactill_api_key == store.tactill_api_key
    assert store_db.pricing_configs == store.pricing_configs


def test_get_stores(
    store_factory: StoreFactory,
    store_repository: StoreRepository,
) -> None:
    stores_count = 4
    limit = 3
    store_factory.create_many(stores_count)

    result = store_repository.get_all(limit=limit)

    assert result.page == 1
    assert result.limit == limit
    assert result.total == stores_count
    assert result.total_pages == (stores_count + limit - 1) // limit
    assert len(result.items) == limit


def test_get_store(
    store_factory: StoreFactory,
    store_repository: StoreRepository,
) -> None:
    stores = store_factory.create_many(3)

    store = stores[0]
    store_db = store_repository.get_by_id(store.id)

    assert store_db
    assert store_db.name == store.name
    assert store_db.slug == store.slug
    assert store_db.tactill_api_key == store.tactill_api_key
    assert store_db.pricing_configs == store.pricing_configs
