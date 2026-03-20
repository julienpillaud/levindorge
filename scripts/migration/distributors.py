import uuid

from rich import print

from app.core.context import Context
from app.domain.articles.entities import Article
from app.domain.metadata.entities.distributors import Distributor
from scripts.migration.utils import to_database_entity

COLLECTION_NAME = "distributors"


def create_distributors(
    src_context: Context,
    dst_context: Context,
    articles: list[Article],
) -> None:
    distributors = src_context.mongo_context.database[COLLECTION_NAME].find().to_list()
    previous_count = len(distributors)

    # Create entities with the new model
    entities = create_entities(articles)

    # Save in the database
    documents = [to_database_entity(entity) for entity in entities]
    dst_context.mongo_context.database[COLLECTION_NAME].insert_many(documents)

    result = dst_context.mongo_context.database[COLLECTION_NAME].find().to_list()
    print(f"Created {len(result)} {COLLECTION_NAME} ({previous_count})")


def create_entities(articles: list[Article]) -> list[Distributor]:
    dst_entities: dict[str, Distributor] = {}
    for article in articles:
        if not article.distributor:
            continue

        if article.distributor not in dst_entities:
            dst_entities[article.distributor] = Distributor(
                id=uuid.uuid7(),
                name=article.distributor,
            )

    return list(dst_entities.values())
