from cleanstack.exceptions import ConflictError, NotFoundError

from app.domain.context import ContextProtocol
from app.domain.deposits.entities import Deposit, DepositCreate
from app.domain.entities import EntityId
from app.domain.exceptions import DepositInUseError


def get_deposits_command(context: ContextProtocol) -> list[Deposit]:
    return context.repository.get_deposits()


def create_deposit_command(
    context: ContextProtocol,
    deposit_create: DepositCreate,
) -> Deposit:
    deposit = Deposit(
        id="",
        category=deposit_create.category,
        deposit_type=deposit_create.deposit_type,
        value=deposit_create.value,
    )

    if context.repository.deposit_exists(deposit=deposit):
        raise ConflictError()

    return context.repository.create_deposit(deposit=deposit)


def delete_deposit_command(context: ContextProtocol, deposit_id: EntityId) -> None:
    deposit = context.repository.get_deposit(deposit_id=deposit_id)
    if not deposit:
        raise NotFoundError()

    if context.repository.deposit_is_used(deposit=deposit):
        raise DepositInUseError(item_name=deposit.name)

    context.repository.delete_deposit(deposit=deposit)
