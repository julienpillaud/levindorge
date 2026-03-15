from abc import ABC
from collections.abc import Iterator
from contextlib import contextmanager

from cleanstack.infrastructure.mongodb.uow import MongoDBContext, MongoDBUnitOfWork
from faker import Faker

from app.domain.entities import DomainEntity
from tests.factories.base import BaseFactory


class BaseMongoFactory[T: DomainEntity](BaseFactory[T], ABC):
    def __init__(self, faker: Faker, context: MongoDBContext) -> None:
        self.faker = faker
        self.context = context
        self.uow = MongoDBUnitOfWork(context=context)

    @contextmanager
    def _persistence_context(self) -> Iterator[None]:
        with self.uow.transaction():
            yield

    def _commit(self) -> None:
        self.uow.commit()
