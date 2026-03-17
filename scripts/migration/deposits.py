import uuid

from rich import print

from app.core.context import Context
from app.domain.articles.entities import Article
from app.domain.categories.entities import Category
from app.domain.commons.category_groups import CATEGORY_GROUPS_MAP
from app.domain.deposits.entities import Deposit, DepositCategory, DepositType
from app.domain.types import DecimalType


def create_deposits(
    dst_context: Context,
    categories: list[Category],
    articles: list[Article],
) -> None:
    # Create deposits with the new entity model
    dst_deposits = create_deposit_entities(
        categories=categories,
        articles=articles,
    )

    # Save deposits in the database
    result = dst_context.deposit_repository.create_many(dst_deposits)

    count = len(result)
    print(f"Created {count} deposits")


def create_deposit_entities(
    categories: list[Category],
    articles: list[Article],
) -> list[Deposit]:
    categories_map = {category.name: category for category in categories}

    dst_deposits: dict[tuple[DecimalType, DepositType, DepositCategory], Deposit] = {}
    for article in articles:
        if not article.deposit:
            continue

        category = categories_map[article.category]
        category_group = CATEGORY_GROUPS_MAP[category.category_group]
        if not category_group.deposit:
            continue

        if article.deposit.unit:
            key = (
                article.deposit.unit,
                DepositType.UNIT,
                category_group.deposit.category,
            )
            if key not in dst_deposits:
                dst_deposits[key] = Deposit(
                    id=uuid.uuid7(),
                    value=article.deposit.unit,
                    type=DepositType.UNIT,
                    category=category_group.deposit.category,
                )

        if article.deposit.case:
            key = (
                article.deposit.case,
                DepositType.CASE,
                category_group.deposit.category,
            )
            if key not in dst_deposits:
                dst_deposits[key] = Deposit(
                    id=uuid.uuid7(),
                    value=article.deposit.case,
                    type=DepositType.CASE,
                    category=category_group.deposit.category,
                )

    return list(dst_deposits.values())
