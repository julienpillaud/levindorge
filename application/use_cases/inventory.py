from pymongo.results import DeleteResult

from application.entities.inventory import (
    CreateOrUpdateInventory,
    Inventory,
    RequestInventory,
)
from utils import mongo_db


class InventoryManager:
    @staticmethod
    def save(request_inventory: RequestInventory) -> Inventory:
        article = mongo_db.get_article_by_id(request_inventory.article_id)

        sale_value = round(request_inventory.stock_quantity * article.taxfree_price, 2)
        deposit_value = 0
        if article.packaging > 0:
            deposit_value = round(
                (request_inventory.stock_quantity / article.packaging)
                * article.deposit.case,
                2,
            )

        inventory_record = CreateOrUpdateInventory(
            article_id=request_inventory.article_id,
            stock_quantity=request_inventory.stock_quantity,
            sale_value=sale_value,
            deposit_value=deposit_value,
        )
        mongo_db.save_inventory_record(inventory_record=inventory_record)
        return mongo_db.get_inventory_record(article_id=request_inventory.article_id)

    @staticmethod
    def reset() -> DeleteResult:
        return mongo_db.reset_inventory()
