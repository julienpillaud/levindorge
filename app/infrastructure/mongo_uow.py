from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import Any

from pymongo import MongoClient

from app.core.config import Settings
from app.domain.domain import UnitOfWorkProtocol


class MongoUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, settings: Settings):
        self.client: MongoClient[Mapping[str, Any]] = MongoClient(settings.MONGODB_URI)
        self.database = self.client[settings.MONGODB_DATABASE]

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield  # transaction is not yet implemented

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass
