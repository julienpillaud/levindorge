from collections import defaultdict
from datetime import datetime, timezone

from tactill.entities.catalog.article import Article as TactillArticle

from application.entities.article import ExtendedArticle
from application.entities.inventory import (
    CreateInventoryRecord,
    CreateInventory,
    Inventory,
    InventoryRecord,
    InventoryValues,
    InventoryDetail,
    UpdateInventory,
)
from application.entities.shop import Shop
from application.interfaces.repository import IRepository


class InventoryManager:
    @staticmethod
    def get_inventories(repository: IRepository) -> list[Inventory]:
        return repository.get_inventories()

    @staticmethod
    def get_inventory(repository: IRepository, inventory_id: str) -> Inventory:
        return repository.get_inventory(inventory_id=inventory_id)

    @staticmethod
    def get_inventory_records(
        repository: IRepository, inventory_id: str
    ) -> list[InventoryRecord]:
        return repository.get_inventory_records(inventory_id=inventory_id)

    @staticmethod
    def save(
        repository: IRepository,
        shop: Shop,
        articles: list[ExtendedArticle],
        tactill_articles: list[TactillArticle],
    ) -> None:
        stocks = {
            article.reference: article.stock_quantity
            for article in tactill_articles
            if article.stock_quantity > 0
        }

        inventory_create = CreateInventory(
            date=datetime.now(timezone.utc),
            shop=shop.name,
        )
        inventory = repository.create_inventory(inventory=inventory_create)
        inventory_id = str(inventory.inserted_id)

        inventory_records = []
        inventory_values_data = defaultdict(InventoryDetail)
        global_sale_value = 0
        global_deposit_value = 0
        for article in articles:
            stock_quantity = stocks.get(article.id)
            if stock_quantity is None:
                continue

            sale_value = round(stock_quantity * article.taxfree_price, 2)
            deposit_value = 0
            if article.packaging > 0:
                deposit_value = round(
                    (stock_quantity / article.packaging) * article.deposit.case, 2
                )

            inventory_values_data[
                article.article_type.list_category
            ].sale_value += sale_value
            global_sale_value += sale_value
            inventory_values_data[
                article.article_type.list_category
            ].deposit_value += deposit_value
            global_deposit_value += deposit_value

            inventory_records.append(
                CreateInventoryRecord(
                    inventory_id=inventory_id,
                    article_id=article.id,
                    article_name=article.name,
                    article_volume=article.volume,
                    article_packaging=article.packaging,
                    article_deposit=article.deposit,
                    article_type=article.type,
                    taxfree_price=article.taxfree_price,
                    stock_quantity=stock_quantity,
                    sale_value=sale_value,
                    deposit_value=deposit_value,
                )
            )

        repository.save_inventory_records(inventory_records=inventory_records)

        inventory_values = InventoryValues.model_validate(inventory_values_data)
        inventory_update = UpdateInventory(
            inventory=inventory_values,
            sale_value=global_sale_value,
            deposit_value=global_deposit_value,
        )
        repository.update_inventory(
            inventory_id=inventory_id, inventory=inventory_update
        )

    @staticmethod
    def delete(repository: IRepository, inventory_id: str) -> None:
        repository.delete_inventory(inventory_id=inventory_id)
        repository.delete_inventory_records(inventory_id=inventory_id)
