from typing import Any

from polyfactory.factories.pydantic_factory import ModelFactory

from app.domain.producers.entities import Producer
from app.infrastructure.repository.producers import ProducerRepository
from tests.factories.base import BaseMongoFactory


class ProducerEntityFactory(ModelFactory[Producer]): ...


class ProducerFactory(BaseMongoFactory[Producer]):
    repository_class = ProducerRepository

    def build(self, **kwargs: Any) -> Producer:
        return ProducerEntityFactory.build(**kwargs)
