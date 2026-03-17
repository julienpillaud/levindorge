import uuid
from typing import Any

from cleanstack.factories.mongo import BaseMongoFactory
from faker import Faker

from app.domain.distributors.entities import Distributor
from app.infrastructure.repository.distributors import DistributorRepository


def generate_distributor(faker: Faker, **kwargs: Any) -> Distributor:
    return Distributor(
        id=kwargs["id"] if "id" in kwargs else uuid.uuid7(),
        name=kwargs["name"] if "name" in kwargs else faker.company(),
    )


class DistributorFactory(BaseMongoFactory[Distributor]):
    def build(self, **kwargs: Any) -> Distributor:
        return generate_distributor(self.faker, **kwargs)

    @property
    def _repository(self) -> DistributorRepository:
        return DistributorRepository(
            database=self.context.database,
            session=self.uow.session,
        )
