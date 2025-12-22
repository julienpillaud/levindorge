from typing import Any

from polyfactory.factories.pydantic_factory import ModelFactory

from app.domain.distributors.entities import Distributor
from app.infrastructure.repository.distributors import DistributorRepository
from tests.factories.base import BaseMongoFactory


class DistributorEntityFactory(ModelFactory[Distributor]): ...


class DistributorFactory(BaseMongoFactory[Distributor]):
    repository_class = DistributorRepository

    def build(self, **kwargs: Any) -> Distributor:
        return DistributorEntityFactory.build(**kwargs)
