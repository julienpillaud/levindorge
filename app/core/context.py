from collections.abc import Iterator
from contextlib import contextmanager

from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo import MongoClient

from app.core.config import Settings
from app.domain.context import ContextProtocol
from app.infrastructure.repository import MongoRepository


class MongoContext(ContextProtocol):
    def __init__(self, settings: Settings) -> None:
        client: MongoClient[MongoDocument] = MongoClient(settings.mongo_uri)
        self.database = client[settings.mongo_database]

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class Context(MongoContext):
    @property
    def repository(self) -> MongoRepository:
        return MongoRepository(database=self.database)
