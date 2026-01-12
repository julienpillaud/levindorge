import pytest

from app.domain.context import ContextProtocol
from app.domain.deposits.commands import create_deposit_command
from app.domain.deposits.entities import DepositCreate
from app.domain.exceptions import AlreadyExistsError
from tests.factories.deposits import DepositFactory


def test_create_deposit(
    context: ContextProtocol,
    deposit_factory: DepositFactory,
) -> None:
    deposit_data = deposit_factory.build()
    deposit_create = DepositCreate(
        value=deposit_data.value,
        type=deposit_data.type,
        category=deposit_data.category,
    )
    deposit = create_deposit_command(context, deposit_create=deposit_create)

    assert deposit.value == deposit_create.value
    assert deposit.type == deposit_create.type
    assert deposit.category == deposit_create.category


def test_create_deposit_already_exists(
    context: ContextProtocol,
    deposit_factory: DepositFactory,
) -> None:
    deposit = deposit_factory.create_one()
    deposit_create = DepositCreate(
        value=deposit.value,
        type=deposit.type,
        category=deposit.category,
    )
    with pytest.raises(AlreadyExistsError):
        create_deposit_command(context, deposit_create=deposit_create)
