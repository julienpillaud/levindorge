from collections.abc import Iterator
from contextlib import contextmanager

from cleanstack.infrastructure.mongo.entities import MongoDocument
from fastapi import FastAPI
from faststream.redis import RedisBroker
from pymongo import MongoClient

from app.core.config import Settings
from app.domain.context import ContextProtocol
from app.domain.domain import Domain
from app.infrastructure.event_publisher import FastStreamEventPublisher
from app.infrastructure.repository import MongoRepository
from app.infrastructure.tactill.manager import TactillManager


class BaseContext(ContextProtocol):
    def __init__(self, settings: Settings) -> None:
        client: MongoClient[MongoDocument] = MongoClient(settings.mongo_uri)
        self.database = client[settings.mongo_database]
        self.broker = RedisBroker(str(settings.redis_dsn))

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class Context(BaseContext):
    @property
    def repository(self) -> MongoRepository:
        return MongoRepository(database=self.database)

    @property
    def pos_manager(self) -> TactillManager:
        return TactillManager()

    @property
    def event_publisher(self) -> FastStreamEventPublisher:
        return FastStreamEventPublisher(broker=self.broker)


def initialize_app(settings: Settings, app: FastAPI) -> None:
    context = Context(settings=settings)
    domain = Domain(context=context)
    app.state.domain = domain
