import pytest

from app.core.config.settings import AppEnvironment, Settings
from app.core.context import Context
from app.core.uow import UnitOfWork
from app.domain.stores.entities import Store
from app.infrastructure.repository.uow import MongoUnitOfWork
from tests.factories.stores import StoreFactory

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.factories",
    "tests.fixtures.repositories",
]


def get_settings_override() -> Settings:
    return Settings(
        app_version="",
        environment=AppEnvironment.TESTING,
        secret_key="",
        supabase_url="",
        supabase_key="",
        jwt_secret="",
        mongo_user=None,
        mongo_password=None,
        mongo_host="localhost",
        mongo_database="test",
        rabbitmq_user="guest",
        rabbitmq_password="guest",
        rabbitmq_host="localhost",
        redis_host="localhost",
        redis_port=6379,
    )


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings_override()


@pytest.fixture
def store(store_factory: StoreFactory) -> Store:
    return store_factory.create_one(name="Store Test", slug="store-test")


@pytest.fixture
def mongo_uow(settings: Settings) -> MongoUnitOfWork:
    return MongoUnitOfWork(settings=settings)


@pytest.fixture
def uow(mongo_uow: MongoUnitOfWork) -> UnitOfWork:
    return UnitOfWork(mongo=mongo_uow)


@pytest.fixture
def context(settings: Settings, uow: UnitOfWork) -> Context:
    context = Context(settings=settings, uow=uow)
    context.cache_manager.flush()
    return context
