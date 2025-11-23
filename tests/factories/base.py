from typing import Any

from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.synchronous.database import Database

from app.domain._shared.protocols.base_repository import RepositoryProtocol
from app.domain.entities import DomainEntity
from app.infrastructure.repository.mongo_repository import MongoRepository


class BaseFactory[T: DomainEntity]:
    repository: RepositoryProtocol[T]

    def build(self, **kwargs: Any) -> T:
        raise NotImplementedError()

    def create_one(self, **kwargs: Any) -> T:
        entity = self.build(**kwargs)
        return self.repository.create(entity)

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:
        return [self.create_one(**kwargs) for _ in range(count)]


class BaseMongoFactory[T: DomainEntity](BaseFactory[T]):
    repository_class: type[MongoRepository[T]]

    def __init__(self, database: Database[MongoDocument]) -> None:
        self.database = database
        self.repository = self.repository_class(database=database)
