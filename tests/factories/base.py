from typing import Any

from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.synchronous.database import Database

from app.domain.entities import DomainEntity
from app.domain.protocols.base_repository import RepositoryProtocol


class BaseFactory[T: DomainEntity]:
    def __init__(self, database: Database[MongoDocument]) -> None:
        self.database = database

    @property
    def repository(self) -> RepositoryProtocol[T]:
        raise NotImplementedError()

    def build(self, **kwargs: Any) -> T:
        raise NotImplementedError()

    def create_one(self, **kwargs: Any) -> T:
        entity = self.build(**kwargs)
        return self.repository.create(entity)

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:
        return [self.create_one(**kwargs) for _ in range(count)]
