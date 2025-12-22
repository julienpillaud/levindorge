from typing import Any

from polyfactory.factories.pydantic_factory import ModelFactory

from app.domain.deposits.entities import Deposit
from app.infrastructure.repository.deposits import DepositRepository
from tests.factories.base import BaseMongoFactory


class DepositEntityFactory(ModelFactory[Deposit]): ...


class DepositFactory(BaseMongoFactory[Deposit]):
    repository_class = DepositRepository

    def build(self, **kwargs: Any) -> Deposit:
        return DepositEntityFactory.build(**kwargs)
