from rich import print

from app.core.core import Context
from app.domain.articles.entities import Article
from app.domain.categories.entities import Category
from app.domain.deposits.entities import Deposit, DepositType


def create_deposits(
    dst_context: Context,
    categories: list[Category],
    articles: list[Article],
) -> None:
    dst_deposits = create_deposit_entities(
        categories=categories,
        articles=articles,
    )
    result = dst_context.deposit_repository.create_many(dst_deposits)
    count = len(result)
    print(f"Created {count} deposits")


def create_deposit_entities(
    categories: list[Category],
    articles: list[Article],
) -> list[Deposit]:
    categories_map = {category.name: category for category in categories}

    dst_deposits: list[Deposit] = []
    for article in articles:
        if not article.deposit:
            continue

        if article.deposit.unit:
            deposit = Deposit(
                value=article.deposit.unit,
                type=DepositType.UNIT,
                category=categories_map[article.category].deposit_category,
            )
            if deposit not in dst_deposits:
                dst_deposits.append(deposit)
        if article.deposit.case:
            deposit = Deposit(
                value=article.deposit.case,
                type=DepositType.CASE,
                category=categories_map[article.category].deposit_category,
            )
            if deposit not in dst_deposits:
                dst_deposits.append(deposit)

    return dst_deposits
