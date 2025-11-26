from collections.abc import Iterator

import pytest
from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import Settings
from app.infrastructure.repository.mongo_repository import MongoDocument


@pytest.fixture
def client(settings: Settings) -> MongoClient[MongoDocument]:
    return MongoClient(settings.mongo_uri)


@pytest.fixture
def database(
    settings: Settings,
    client: MongoClient[MongoDocument],
) -> Iterator[Database[MongoDocument]]:
    mongo_database = client[settings.mongo_database]
    yield mongo_database
    for collection in mongo_database.list_collection_names():
        mongo_database.drop_collection(collection)
