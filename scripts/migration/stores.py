import uuid
from typing import Any

from rich import print

from app.core.context import Context
from app.domain.stores.entities import Store
from data.stores import PRICING_CONFIG
from scripts.migration.utils import to_database_entity

COLLECTION_NAME = "stores"


def create_stores(src_context: Context, dst_context: Context) -> list[Store]:
    # Get previous stores
    src_stores = src_context.mongo_context.database["shops"].find().to_list()

    # Create entities with the new model
    entities = create_entities(src_stores)

    # Save in the database
    documents = [to_database_entity(entity) for entity in entities]
    dst_context.mongo_context.database[COLLECTION_NAME].insert_many(documents)

    result = dst_context.store_repository.get_all().items
    print(f"Created {len(result)} {COLLECTION_NAME} ({len(src_stores)})")
    return result


def create_entities(src_stores: list[dict[str, Any]]) -> list[Store]:
    return [
        Store(
            id=uuid.uuid7(),
            name=store["name"],
            slug=store["username"],
            tactill_api_key=store["tactill_api_key"],
            # All stores have the same pricing config
            pricing_configs=PRICING_CONFIG,
        )
        for store in src_stores
    ]
