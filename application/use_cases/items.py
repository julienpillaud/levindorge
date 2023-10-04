from application.entities.item import Item, RequestItem
from utils import mongo_db


class ItemManager:
    @staticmethod
    def list(category: str) -> list[Item]:
        return mongo_db.get_items(category=category)

    @staticmethod
    def create(category: str, request_item: RequestItem) -> Item:
        insert_result = mongo_db.create_item(category=category, item=request_item)
        return mongo_db.get_item_by_id(
            category=category, item_id=insert_result.inserted_id
        )

    @staticmethod
    def delete(category: str, item_id: str) -> None:
        mongo_db.delete_item(category=category, item_id=item_id)
