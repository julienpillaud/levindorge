import datetime
from collections import defaultdict
from typing import Any

from cleanstack.exceptions import NotFoundError

from app.domain.context import ContextProtocol
from app.domain.entities import EntityId
from app.domain.inventories.entities import (
    Inventory,
    InventoryDetail,
    InventoryRecord,
    InventoryReport,
)
from app.domain.stores.entities import Store


def get_inventories_command(context: ContextProtocol) -> list[Inventory]:
    return context.repository.get_inventories()


def get_inventory_command(
    context: ContextProtocol,
    inventory_id: EntityId,
) -> InventoryReport:
    inventory = context.repository.get_inventory_report(inventory_id=inventory_id)
    if not inventory:
        raise NotFoundError()

    return inventory


def create_inventory_command(context: ContextProtocol, store: Store) -> Inventory:
    results = context.article_repository.get_all(sort={"type": 1}, page=1, limit=1000)
    articles = results.items
    # TODO : get from category repository
    article_types_mapping: dict[str, Any] = {}
    # article_types_mapping = {
    #     article_type.name: article_type
    #     for article_type in context.repository.get_article_types()
    # }
    pos_articles = context.pos_manager.get_articles(store)
    stock_quantity_mapping = {
        article.reference: article.stock_quantity
        for article in pos_articles
        if article.stock_quantity > 0
    }

    records = []
    for article in articles:
        stock_quantity = stock_quantity_mapping.get(article.id)
        if stock_quantity is None:
            continue

        records.append(
            InventoryRecord(
                inventory_id="",
                article_id=article.id,
                article_name=article.display_name,
                article_volume=article.volume.value if article.volume else 0.0,
                article_packaging=article.packaging,
                article_deposit=article.deposit,
                article_type=article.category,
                taxfree_price=article.total_cost,
                stock_quantity=stock_quantity,
                sale_value=article.inventory_value(stock_quantity),
                deposit_value=article.deposit_value(stock_quantity),
            )
        )

    inventory_details: defaultdict[str, InventoryDetail] = defaultdict(InventoryDetail)
    for record in records:
        article_type = article_types_mapping[record.article_type]
        inventory_details[article_type.display_group].add(
            inventory_value=record.sale_value,
            deposit_value=record.deposit_value,
        )

    inventory_create = Inventory(
        id="",
        date=datetime.datetime.now(datetime.UTC),
        shop=store.name,
        inventory=inventory_details,
        sale_value=sum(value.sale_value for value in inventory_details.values()),
        deposit_value=sum(value.deposit_value for value in inventory_details.values()),
    )
    inventory = context.repository.create_inventory(inventory=inventory_create)
    context.repository.create_inventory_records(
        inventory_id=inventory.id,
        records=records,
    )
    return inventory


def delete_inventory_command(context: ContextProtocol, inventory_id: EntityId) -> None:
    inventory = context.repository.get_inventory(inventory_id=inventory_id)
    if not inventory:
        raise NotFoundError()

    context.repository.delete_inventory(inventory=inventory)
    context.repository.delete_inventory_records(inventory_id=inventory_id)
