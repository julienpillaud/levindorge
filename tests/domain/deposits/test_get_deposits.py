from app.domain.context import ContextProtocol
from app.domain.deposits.commands import get_deposits_command
from app.domain.deposits.entities import DepositCategory
from tests.factories.deposits import DepositFactory


def test_get_deposits(
    context: ContextProtocol,
    deposit_factory: DepositFactory,
) -> None:
    deposits_count = 3
    deposit_factory.create_many(deposits_count)

    result = get_deposits_command(context)

    assert result.total == deposits_count
    deposits = result.items
    assert len(deposits) == deposits_count


def test_get_deposits_by_category(
    context: ContextProtocol,
    deposit_factory: DepositFactory,
) -> None:
    deposits_count = 3
    deposit_factory.create_many(deposits_count, category=DepositCategory.KEG)
    deposit_factory.create_one(category=DepositCategory.BEER)

    result = get_deposits_command(context, category=DepositCategory.BEER)

    assert result.total == 1
    deposits = result.items
    assert len(deposits) == 1
