from decimal import Decimal

import pytest
from bson import ObjectId
from cleanstack.exceptions import NotFoundError

from app.domain.articles.entities import ArticleDeposit
from app.domain.context import ContextProtocol
from app.domain.deposits.commands import delete_deposit_command
from app.domain.deposits.entities import DepositCategory, DepositType
from app.domain.exceptions import EntityInUseError
from tests.factories.articles import ArticleFactory
from tests.factories.deposits import DepositFactory


def test_delete_deposit(
    context: ContextProtocol,
    deposit_factory: DepositFactory,
) -> None:
    deposit = deposit_factory.create_one()

    delete_deposit_command(context, deposit_id=deposit.id)

    assert context.deposit_repository.get_by_id(deposit.id) is None


def test_delete_deposit_not_found(context: ContextProtocol) -> None:
    with pytest.raises(NotFoundError):
        delete_deposit_command(context, deposit_id=str(ObjectId()))


def test_delete_deposit_in_use(
    context: ContextProtocol,
    article_factory: ArticleFactory,
    deposit_factory: DepositFactory,
) -> None:
    article_deposit = ArticleDeposit(
        unit=Decimal("0.1"),
        case=Decimal("4.5"),
        packaging=12,
    )
    article_factory.create_one(deposit=article_deposit)
    deposit = deposit_factory.create_one(
        value=article_deposit.unit,
        type=DepositType.UNIT,
        category=DepositCategory.BEER,
    )
    with pytest.raises(EntityInUseError):
        delete_deposit_command(context, deposit_id=deposit.id)
