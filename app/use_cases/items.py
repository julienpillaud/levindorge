from app.entities.item import Item, RequestItem
from app.interfaces.repository import IRepository


class ItemManager:
    @staticmethod
    def list(repository: IRepository, category: str) -> list[Item]:
        return repository.get_items(category=category)

    @staticmethod
    def create(
        repository: IRepository, category: str, request_item: RequestItem
    ) -> Item:
        insert_result = repository.create_item(category=category, item=request_item)
        return repository.get_item_by_id(
            category=category, item_id=insert_result.inserted_id
        )

    @staticmethod
    def delete(repository: IRepository, category: str, item_id: str) -> None:
        repository.delete_item(category=category, item_id=item_id)
