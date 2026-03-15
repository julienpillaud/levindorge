from abc import ABC, abstractmethod
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from app.domain.entities import DomainEntity
from app.domain.protocols.repository import RepositoryProtocol


class BaseFactory[T: DomainEntity](ABC):
    def create_one(self, **kwargs: Any) -> T:
        entity = self.build(**kwargs)
        with self._persistence_context():
            created = self._repository.create(entity)
            self._commit()
            return created

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:
        entities = [self.build(**kwargs) for _ in range(count)]
        created_entities: list[T] = []
        with self._persistence_context():
            for entity in entities:
                created = self._repository.create(entity)
                created_entities.append(created)
            self._commit()
        return created_entities

    @abstractmethod
    def build(self, **kwargs: Any) -> T: ...

    @abstractmethod
    def _commit(self) -> None: ...

    @contextmanager
    @abstractmethod
    def _persistence_context(self) -> Iterator[None]: ...

    @property
    @abstractmethod
    def _repository(self) -> RepositoryProtocol[T]: ...
