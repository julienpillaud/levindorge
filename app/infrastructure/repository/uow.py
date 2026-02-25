from collections.abc import Iterator
from contextlib import contextmanager

from cleanstack.uow import UnitOfWorkProtocol
from pymongo import MongoClient

from app.core.config.settings import Settings
from app.infrastructure.repository.provider import MongoProvider
from app.infrastructure.repository.types import MongoDocument


class MongoUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, settings: Settings) -> None:
        MongoProvider.init(settings)
        self.client: MongoClient[MongoDocument] = MongoProvider.get_client()
        self.database = self.client[settings.mongo_database]

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass
