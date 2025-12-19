from typing import Any

from rich import print

from app.core.core import Context
from app.domain.articles.entities import ArticleDeposit
from app.domain.commons.entities import InventoryGroup
from app.domain.inventories.entities import Inventory, InventoryDetail, InventoryRecord
from app.domain.stores.entities import Store


def create_inventories(
    src_context: Context,
    dst_context: Context,
    stores: list[Store],
) -> None:
    # Get previous inventories
    src_inventories = list(src_context.database["inventories"].find())
    # Create inventories with the new entity model
    inventories = create_inventories_entities(
        src_inventories=src_inventories,
        stores=stores,
    )

    # Save inventories in the database
    dst_inventories = [inventory.model_dump() for inventory in inventories]
    result = dst_context.database["inventories"].insert_many(dst_inventories)
    print(f"Created {len(result.inserted_ids)} inventories ({len(src_inventories)})")

    # Get previous inventory records
    src_inventory_records = list(src_context.database["inventory_records"].find())
    # Create inventory records with the new entity model
    inventory_records = create_inventory_record_entities(src_inventory_records)
    dst_inventory_records = [
        record.model_dump(exclude={"id"}) for record in inventory_records
    ]
    result = dst_context.database["inventory_records"].insert_many(
        dst_inventory_records
    )
    print(
        f"Created {len(result.inserted_ids)} inventory records "
        f"({len(src_inventory_records)})"
    )


def create_inventories_entities(
    src_inventories: list[dict[str, Any]],
    stores: list[Store],
) -> list[Inventory]:
    stores_map = {store.name: store for store in stores}
    return [
        Inventory(
            # Need to keep previous id
            id=str(inventory["_id"]),
            date=inventory["date"],
            store=stores_map[inventory["shop"]].name,
            inventory=get_inventory_details(inventory),
            inventory_value=inventory["sale_value"],
            deposit_value=inventory["deposit_value"] or None,
        )
        for inventory in src_inventories
    ]


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
    src_inventory_records: list[dict[str, Any]],
) -> list[InventoryRecord]:
    return [
        InventoryRecord(
            inventory_id=record["inventory_id"],
            category=record["article_type"],
            display_name=get_display_name(record),
            total_cost=record["taxfree_price"],
            deposit=get_deposit(record),
            stock_quantity=record["stock_quantity"],
            inventory_value=record["sale_value"],
            deposit_value=record["deposit_value"] or None,
        )
        for record in src_inventory_records
    ]


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


def get_deposit(record: dict[str, Any], /) -> ArticleDeposit | None:
    deposit = record["article_deposit"]
    packaging = record["article_packaging"] or None

    if not deposit["unit"]:
        return None

    return ArticleDeposit(
        unit=deposit["unit"],
        case=deposit["case"] or None,
        packaging=packaging,
    )
