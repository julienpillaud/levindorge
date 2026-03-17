import uuid

from cleanstack.domain import NotFoundError
from cleanstack.entities import (
    EntityId,
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
    SortOrder,
)

from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.deposits.entities import Deposit, DepositCategory, DepositCreate
from app.domain.exceptions import AlreadyExistsError, EntityInUseError
from app.domain.logger import logger


@cached_command(response_model=PaginatedResponse[Deposit], tag="deposits")
def get_deposits_command(
    context: ContextProtocol,
    /,
    category: DepositCategory | None = None,
) -> PaginatedResponse[Deposit]:
    filters = [FilterEntity(field="category", value=category)] if category else []
    return context.deposit_repository.get_all(
        filters=filters,
        sort=[
            SortEntity(field="type", order=SortOrder.ASC),
            SortEntity(field="value", order=SortOrder.ASC),
        ],
        pagination=Pagination(page=1, size=300),
    )


def create_deposit_command(
    context: ContextProtocol,
    /,
    deposit_create: DepositCreate,
) -> Deposit:
    deposit = Deposit(
        id=uuid.uuid7(),
        value=deposit_create.value,
        type=deposit_create.type,
        category=deposit_create.category,
    )
    if context.deposit_repository.exists(deposit):
        raise AlreadyExistsError(
            f"`{deposit.display_name}` already exists.",
            deposit.display_name,
        )

    created_deposit = context.deposit_repository.create(deposit)
    context.cache_manager.invalidate_tag("deposits")
    return created_deposit


def delete_deposit_command(context: ContextProtocol, /, deposit_id: EntityId) -> None:
    logger.info("START COMMAND")
    deposit = context.deposit_repository.get_by_id(deposit_id)
    if not deposit:
        raise NotFoundError(f"Deposit `{deposit_id}` not found.")

    if context.article_repository.exists_by_deposit(deposit):
        raise EntityInUseError(
            f"`{deposit.display_name}` is still in use.",
            deposit.display_name,
        )

    context.deposit_repository.delete(deposit)
    context.cache_manager.invalidate_tag("deposits")
    logger.info("END COMMAND")
