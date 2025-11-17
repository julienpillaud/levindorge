import pytest
from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.database import Database

from app.infrastructure.repository.stores import StoreRepository


@pytest.fixture
def store_repository(database: Database[MongoDocument]) -> StoreRepository:
    return StoreRepository(database=database)
