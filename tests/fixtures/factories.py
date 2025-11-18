import pytest
from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.database import Database

from tests.factories.categories import CategoryFactory
from tests.factories.stores import StoreFactory
from tests.factories.users import UserFactory


@pytest.fixture
def store_factory(database: Database[MongoDocument]) -> StoreFactory:
    return StoreFactory(database=database)


@pytest.fixture
def user_factory(database: Database[MongoDocument]) -> UserFactory:
    return UserFactory(database=database)


@pytest.fixture
def category_factory(database: Database[MongoDocument]) -> CategoryFactory:
    return CategoryFactory(database=database)
