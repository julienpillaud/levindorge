import random
import uuid
from typing import Any

from cleanstack.factories.mongo import BaseMongoFactory

from app.domain.metadata.entities.deposits import Deposit, DepositType
from app.infrastructure.repository.deposits import DepositRepository
from tests.factories.utils import generate_decimal


def generate_deposit(**kwargs: Any) -> Deposit:
    return Deposit(
        id=kwargs["id"] if "id" in kwargs else uuid.uuid7(),
        value=kwargs["value"]
        if "value" in kwargs
        else generate_decimal(decimal_places=2),
        type=kwargs["type"] if "type" in kwargs else random.choice(list(DepositType)),
    )


class DepositFactory(BaseMongoFactory[Deposit]):
    def build(self, **kwargs: Any) -> Deposit:
        return generate_deposit(**kwargs)

    @property
    def _repository(self) -> DepositRepository:
        return DepositRepository(
            database=self.context.database,
            session=self.uow.session,
        )
