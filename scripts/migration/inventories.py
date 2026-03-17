import uuid
from typing import Any

from app.core.context import Context
from app.domain.articles.entities import Article
from app.domain.commons.entities import InventoryGroup
from app.domain.inventories.entities import Inventory, InventoryDetail, InventoryRecord
from app.domain.stores.entities import Store


def create_inventories(
    src_context: Context,
    dst_context: Context,
    stores: list[Store],
    articles_mapping: dict[str, Article],
) -> None:
    # Get previous inventories
    pipeline = [
        {"$addFields": {"str_id": {"$toString": "$_id"}}},
        {
            "$lookup": {
                "from": "inventory_records",
                "localField": "str_id",
                "foreignField": "inventory_id",
                "as": "records",
            }
        },
    ]
    src_inventories = (
        src_context.mongo_context.database["inventories"].aggregate(pipeline).to_list()
    )

    stores_map = {store.name: store for store in stores}
    for src_inventory in src_inventories:
        inventory_id = uuid.uuid7()

        dst_inventory = create_inventory_entity(
            stores_map=stores_map,
            src_inventory=src_inventory,
            inventory_id=inventory_id,
        )
        dst_context.inventory_repository.create(dst_inventory)

        dst_inventory_records = create_inventory_record_entities(
            articles_mapping=articles_mapping,
            src_inventory=src_inventory,
            inventory_id=inventory_id,
        )
        dst_context.inventory_repository.create_records(dst_inventory_records)


def create_inventory_entity(
    stores_map: dict[str, Store],
    src_inventory: dict[str, Any],
    inventory_id: uuid.UUID,
) -> Inventory:
    return Inventory(
        id=inventory_id,
        created_at=src_inventory["date"],
        store=stores_map[src_inventory["shop"]].name,
        inventory=get_inventory_details(src_inventory),
        inventory_value=src_inventory["sale_value"],
        deposit_value=src_inventory["deposit_value"] or None,
    )


def get_inventory_details(
    inventory_dict: dict[str, Any],
    /,
) -> dict[InventoryGroup, InventoryDetail]:
    dst_inventory_details: dict[InventoryGroup, InventoryDetail] = {}
    for key, value in inventory_dict["inventory"].items():
        inventory_group = get_inventory_group(key)
        deposit_value = value["deposit_value"] if value["deposit_value"] != 0 else None
        dst_inventory_details[inventory_group] = InventoryDetail(
            inventory_value=value["sale_value"],
            deposit_value=deposit_value,
        )
    return dst_inventory_details


def get_inventory_group(key: str, /) -> InventoryGroup:
    match key:
        case "rhum":
            return InventoryGroup.RUM
        case "misc":
            return InventoryGroup.OTHER
        case _:
            return InventoryGroup[key.upper()]


def create_inventory_record_entities(
    articles_mapping: dict[str, Article],
    src_inventory: dict[str, Any],
    inventory_id: uuid.UUID,
) -> list[InventoryRecord]:
    inventory_records: list[InventoryRecord] = []
    for record in src_inventory["records"]:
        article = articles_mapping.get(record["article_id"])

        article_id = article.id if article else None
        article_name = get_display_name(record)

        inventory_record = InventoryRecord(
            id=uuid.uuid7(),
            inventory_id=inventory_id,
            article_id=article_id,
            article_name=article_name,
            stock_quantity=record["stock_quantity"],
            inventory_value=record["sale_value"],
            deposit_value=record["deposit_value"] or None,
        )
        inventory_records.append(inventory_record)

    return inventory_records


def get_display_name(record: dict[str, Any], /) -> str:
    name1 = record["article_name"]["name1"]
    name2 = record["article_name"]["name2"]
    volume = record["article_volume"]

    name = ""
    if name1:
        name += name1
    if name2:
        name += f" {name2}"
    if volume:
        name += f" {convert_volume(volume)}"
    return name


def convert_volume(value: int, /) -> str:
    if value >= 100:  # noqa: PLR2004
        return f"{value / 100} L"
    return f"{value} cL"


# def get_deposit(record: dict[str, Any], /) -> ArticleDeposit | None:
#     deposit = record["article_deposit"]
#     packaging = record["article_packaging"] or None
#
#     if not deposit["unit"]:
#         return None
#
#     return ArticleDeposit(
#         unit=deposit["unit"],
#         case=deposit["case"] or None,
#         packaging=packaging,
#     )
