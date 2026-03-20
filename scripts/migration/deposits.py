import uuid

from rich import print

from app.core.context import Context
from app.domain.articles.entities import Article
from app.domain.metadata.entities.deposits import Deposit, DepositType, DepositValue
from scripts.migration.utils import to_database_entity

COLLECTION_NAME = "deposits"


def create_deposits(
    src_context: Context,
    dst_context: Context,
    articles: list[Article],
) -> None:
    deposits = src_context.mongo_context.database[COLLECTION_NAME].find().to_list()
    previous_count = len(deposits)

    # Create entities with the new model
    entities = create_entities(articles)

    # Save in the database
    documents = [to_database_entity(entity) for entity in entities]
    dst_context.mongo_context.database[COLLECTION_NAME].insert_many(documents)

    result = dst_context.mongo_context.database[COLLECTION_NAME].find().to_list()
    print(f"Created {len(result)} {COLLECTION_NAME} ({previous_count})")


def create_entities(articles: list[Article], /) -> list[Deposit]:
    dst_entities: dict[tuple[DepositValue, DepositType], Deposit] = {}
    for article in articles:
        if not article.deposit:
            continue

        if article.deposit.unit:
            key = (article.deposit.unit, DepositType.UNIT)
            if key not in dst_entities:
                dst_entities[key] = Deposit(
                    id=uuid.uuid7(),
                    value=article.deposit.unit,
                    type=DepositType.UNIT,
                )

        if article.deposit.case:
            key = (article.deposit.case, DepositType.CASE)
            if key not in dst_entities:
                dst_entities[key] = Deposit(
                    id=uuid.uuid7(),
                    value=article.deposit.case,
                    type=DepositType.CASE,
                )

    return list(dst_entities.values())
