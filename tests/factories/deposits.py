import random
from typing import Any

from app.domain.deposits.entities import Deposit, DepositCategory, DepositType
from app.infrastructure.repository.deposits import DepositRepository
from tests.factories.base import BaseMongoFactory
from tests.factories.utils import generate_decimal


def generate_deposit(**kwargs: Any) -> Deposit:
    return Deposit(
        value=kwargs["value"]
        if "value" in kwargs
        else generate_decimal(decimal_places=2),
        type=kwargs["type"] if "type" in kwargs else random.choice(list(DepositType)),
        category=kwargs["category"]
        if "category" in kwargs
        else random.choice(list(DepositCategory)),
    )


class DepositFactory(BaseMongoFactory[Deposit]):
    repository_class = DepositRepository

    def build(self, **kwargs: Any) -> Deposit:
        return generate_deposit(**kwargs)
