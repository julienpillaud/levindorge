import uuid

from rich import print

from app.core.context import Context
from app.domain.articles.entities import Article
from app.domain.categories.entities import Category
from app.domain.commons.category_groups import CATEGORY_GROUPS_MAP
from app.domain.metadata.entities.producers import Producer, ProducerType
from scripts.migration.utils import to_database_entity

COLLECTION_NAME = "producers"


def create_producers(
    src_context: Context,
    dst_context: Context,
    articles: list[Article],
    categories: list[Category],
) -> None:
    breweries = src_context.mongo_context.database["breweries"].find().to_list()
    distilleries = src_context.mongo_context.database["distilleries"].find().to_list()
    previous_count = len(breweries) + len(distilleries)

    # Create entities with the new model
    entities = create_entities(articles, categories=categories)

    # Save in the database
    documents = [to_database_entity(entity) for entity in entities]
    dst_context.mongo_context.database[COLLECTION_NAME].insert_many(documents)

    result = dst_context.mongo_context.database[COLLECTION_NAME].find().to_list()
    print(f"Created {len(result)} {COLLECTION_NAME} ({previous_count})")


def create_entities(
    articles: list[Article],
    /,
    categories: list[Category],
) -> list[Producer]:
    categories_map = {category.name: category for category in categories}

    dst_entities: dict[tuple[str, ProducerType | None], Producer] = {}
    for article in articles:
        if not article.producer:
            continue

        category = categories_map[article.category]
        category_group = CATEGORY_GROUPS_MAP[category.category_group]
        if not category_group.producer:
            continue

        key = (article.producer, category_group.producer.type)
        if key not in dst_entities:
            dst_entities[key] = Producer(
                id=uuid.uuid7(),
                name=article.producer,
                type=category_group.producer.type,
            )

    return list(dst_entities.values())
