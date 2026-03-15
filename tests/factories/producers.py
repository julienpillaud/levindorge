import random
from typing import Any

from faker import Faker

from app.domain.producers.entities import Producer, ProducerType
from app.infrastructure.repository.producers import ProducerRepository
from tests.factories.mongo import BaseMongoFactory


def generate_producer(faker: Faker, **kwargs: Any) -> Producer:
    return Producer(
        name=kwargs["name"] if "name" in kwargs else faker.word(),
        type=kwargs["type"] if "type" in kwargs else random.choice(list(ProducerType)),
    )


class ProducerFactory(BaseMongoFactory[Producer]):
    def build(self, **kwargs: Any) -> Producer:
        return generate_producer(self.faker, **kwargs)

    @property
    def _repository(self) -> ProducerRepository:
        return ProducerRepository(
            database=self.context.database,
            session=self.uow.session,
        )
