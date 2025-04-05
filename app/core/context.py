from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import Settings
from app.domain.domain import TransactionalContextProtocol
from app.infrastructure.repository import MongoRepository


class Context(TransactionalContextProtocol):
    def __init__(self, settings: Settings):
        self.client: MongoClient[dict[str, Any]] = MongoClient(settings.MONGODB_URI)
        self.database: Database[dict[str, Any]] = self.client[settings.MONGODB_DATABASE]

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield  # transaction is not yet implemented

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    @property
    def repository(self) -> MongoRepository:
        return MongoRepository(database=self.database)
