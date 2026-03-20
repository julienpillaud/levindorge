import uuid

from rich import print

from app.core.context import Context
from app.domain.articles.entities import Article
from app.domain.metadata.entities.origins import Origin, OriginType
from scripts.migration.utils import to_database_entity

COLLECTION_NAME = "origins"


def create_origins(
    src_context: Context,
    dst_context: Context,
    articles: list[Article],
) -> None:
    countries = src_context.mongo_context.database["countries"].find().to_list()
    regions = src_context.mongo_context.database["regions"].find().to_list()
    previous_count = len(countries) + len(regions)

    # Create entities with the new model
    entities = create_entities(articles)

    # Save in the database
    documents = [to_database_entity(entity) for entity in entities]
    dst_context.mongo_context.database[COLLECTION_NAME].insert_many(documents)

    result = dst_context.mongo_context.database[COLLECTION_NAME].find().to_list()
    print(f"Created {len(result)} {COLLECTION_NAME} ({previous_count})")


def create_entities(articles: list[Article], /) -> list[Origin]:
    dst_entities: dict[tuple[str, str | None, OriginType], Origin] = {}
    for article in articles:
        if not article.origin:
            continue

        key = (article.origin.name, article.origin.code, article.origin.type)
        if key not in dst_entities:
            dst_entities[key] = Origin(
                id=uuid.uuid7(),
                name=article.origin.name,
                code=article.origin.code,
                type=OriginType(article.origin.type),
            )

    return list(dst_entities.values())
