from app.infrastructure.repository.users import UserRepository
from tests.factories.stores import StoreFactory
from tests.factories.users import UserFactory
from tests.utils import is_str_object_id


def test_create_user(
    store_factory: StoreFactory,
    user_factory: UserFactory,
    user_repository: UserRepository,
) -> None:
    stores = store_factory.create_many(2)
    user = user_factory.build(stores=stores)

    user_db = user_repository.create(user)

    assert is_str_object_id(user_db.id)
    assert user_db.name == user.name
    assert user_db.email == user.email
    assert user_db.hashed_password == user.hashed_password
    assert user_db.stores == user.stores
    assert user_db.role == user.role


def test_get_users(
    user_factory: UserFactory,
    user_repository: UserRepository,
) -> None:
    items_count = 4
    limit = 3
    user_factory.create_many(items_count)

    result = user_repository.get_all(limit=limit)

    assert result.page == 1
    assert result.limit == limit
    assert result.total == items_count
    assert result.total_pages == (items_count + limit - 1) // limit
    assert len(result.items) == limit


def test_get_user(
    store_factory: StoreFactory,
    user_factory: UserFactory,
    user_repository: UserRepository,
) -> None:
    stores = store_factory.create_many(2)
    users = user_factory.create_many(3, stores=stores)

    user = users[0]
    user_db = user_repository.get_by_id(user.id)

    assert user_db
    assert is_str_object_id(user_db.id)
    assert user_db.name == user.name
    assert user_db.email == user.email
    assert user_db.hashed_password == user.hashed_password
    assert user_db.stores == user.stores
    assert user_db.role == user.role
