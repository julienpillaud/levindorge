import uuid
from typing import Any

from cleanstack.entities import Pagination
from rich import print

from app.core.context import Context
from app.domain.stores.entities import Store
from data.stores import PRICING_CONFIG


def create_stores(src_context: Context, dst_context: Context) -> list[Store]:
    # Get previous stores
    src_stores = src_context.mongo_context.database["shops"].find().to_list()
    # Create stores with the new entity model
    dst_stores = create_store_entities(src_stores)

    # Save stores in the database
    result = dst_context.store_repository.create_many(dst_stores)

    count = len(result)
    print(f"Created {count} stores ({len(src_stores)})")

    return dst_context.store_repository.get_all(
        pagination=Pagination(page=1, size=count)
    ).items


def create_store_entities(src_stores: list[dict[str, Any]]) -> list[Store]:
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
