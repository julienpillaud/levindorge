from pymongo.results import DeleteResult

from application.entities.inventory import (
    CreateOrUpdateInventory,
    Inventory,
    RequestInventory,
)
from application.interfaces.repository import IRepository


class InventoryManager:
    @staticmethod
    def save(repository: IRepository, request_inventory: RequestInventory) -> Inventory:
        article = repository.get_article_by_id(request_inventory.article_id)

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
        repository.save_inventory_record(inventory_record=inventory_record)
        return repository.get_inventory_record(article_id=request_inventory.article_id)

    @staticmethod
    def reset(repository: IRepository) -> DeleteResult:
        return repository.reset_inventory()
