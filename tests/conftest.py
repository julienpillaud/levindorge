import pytest

from app.core.config.settings import AppEnvironment, Settings
from app.core.core import Context
from app.domain.stores.entities import Store
from app.domain.users.entities import User
from tests.factories.stores import StoreFactory
from tests.factories.users import UserFactory

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.factories",
    "tests.fixtures.repositories",
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings(
        app_version="",
        environment=AppEnvironment.TESTING,
        secret_key="",
        mongo_user="user",
        mongo_password="password",
        mongo_host="localhost",
        mongo_port=27017,
        mongo_database="test",
        redis_host="localhost",
        redis_port=6379,
    )


@pytest.fixture
def store(store_factory: StoreFactory) -> Store:
    return store_factory.create_one(name="Store Test", slug="store-test")


@pytest.fixture
def current_user(user_factory: UserFactory, store: Store) -> User:
    return user_factory.create_one(stores=[store])


@pytest.fixture(scope="session")
def context(settings: Settings) -> Context:
    return Context(settings=settings)
