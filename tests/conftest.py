from collections.abc import Iterator

import pytest
from cleanstack.domain import CompositeUniOfWork
from cleanstack.infrastructure.mongo.uow import MongoContext, MongoUnitOfWork

from app.core.config.settings import AppEnvironment, Settings
from app.core.context import Context
from app.domain.stores.entities import Store
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
        mongo_rs_name="rs0",
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
def mongo_uow(mongo_context: MongoContext) -> MongoUnitOfWork:
    return MongoUnitOfWork(context=mongo_context)


@pytest.fixture
def uow(mongo_uow: MongoUnitOfWork) -> Iterator[CompositeUniOfWork]:
    uow = CompositeUniOfWork(members=[mongo_uow])
    with uow.transaction():
        yield uow


@pytest.fixture
def context(
    settings: Settings,
    mongo_context: MongoContext,
    mongo_uow: MongoUnitOfWork,
    uow: Iterator[CompositeUniOfWork],
) -> Context:
    context = Context(
        settings=settings,
        mongo_context=mongo_context,
        mongo_uow=mongo_uow,
    )
    context.cache_manager.flush()
    return context
