from typing import Any

from faker import Faker

from app.domain.distributors.entities import Distributor
from app.infrastructure.repository.distributors import DistributorRepository
from tests.factories.base import BaseMongoFactory


def generate_distributor(faker: Faker, **kwargs: Any) -> Distributor:
    return Distributor(name=kwargs["name"] if "name" in kwargs else faker.company())


class DistributorFactory(BaseMongoFactory[Distributor]):
    repository_class = DistributorRepository

    def build(self, **kwargs: Any) -> Distributor:
        return generate_distributor(self.faker, **kwargs)
