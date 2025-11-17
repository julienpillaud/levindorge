import pytest
from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.database import Database

from tests.factories.stores import StoreFactory


@pytest.fixture
def store_factory(database: Database[MongoDocument]) -> StoreFactory:
    return StoreFactory(collection=database["stores"])
