from app.domain.context import ContextProtocol
from app.domain.deposits.entities import Deposit, DepositCategory
from app.domain.entities import PaginatedResponse


def get_deposits_command(
    context: ContextProtocol,
    deposit_category: DepositCategory | None = None,
) -> PaginatedResponse[Deposit]:
    filters = {"category": deposit_category} if deposit_category else {}
    return context.deposit_repository.get_all(
        filters=filters,
        sort={"type": 1, "value": 1},
        limit=300,
    )
