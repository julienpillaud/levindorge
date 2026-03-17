from collections.abc import Iterator

import pytest
from cleanstack.infrastructure.mongo.uow import MongoContext

from app.core.config.settings import Settings


@pytest.fixture(scope="session")
def mongo_context(settings: Settings) -> MongoContext:
    return MongoContext.from_settings(
        host=settings.mongo_uri,
        database_name=settings.mongo_database,
    )


@pytest.fixture(autouse=True)
def clean_mongo(mongo_context: MongoContext) -> Iterator[None]:
    yield
    database = mongo_context.database
    for collection in database.list_collection_names():
        database[collection].delete_many({})
