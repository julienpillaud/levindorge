import uuid

from pydantic import PositiveFloat
from rich import print

from app.core.context import Context
from app.domain.articles.entities import Article
from app.domain.metadata.entities.volumes import Volume, VolumeUnit
from scripts.migration.utils import to_database_entity

COLLECTION_NAME = "volumes"


def create_volume(
    src_context: Context,
    dst_context: Context,
    articles: list[Article],
) -> None:
    volumes = src_context.mongo_context.database[COLLECTION_NAME].find().to_list()
    previous_count = len(volumes)

    # Create entities with the new model
    entities = create_entities(articles)

    # Save in the database
    documents = [to_database_entity(entity) for entity in entities]
    dst_context.mongo_context.database[COLLECTION_NAME].insert_many(documents)

    result = dst_context.mongo_context.database[COLLECTION_NAME].find().to_list()
    print(f"Created {len(result)} {COLLECTION_NAME} ({previous_count})")


def create_entities(articles: list[Article], /) -> list[Volume]:
    dst_entities: dict[tuple[PositiveFloat, VolumeUnit], Volume] = {}
    for article in articles:
        if not article.volume:
            continue

        key = (article.volume.value, article.volume.unit)
        if key not in dst_entities:
            dst_entities[key] = Volume(
                id=uuid.uuid7(),
                value=article.volume.value,
                unit=VolumeUnit(article.volume.unit),
            )

    return list(dst_entities.values())
