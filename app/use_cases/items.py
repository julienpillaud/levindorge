from pymongo.results import DeleteResult

from app.entities.deposit import RequestDeposit, Deposit
from app.entities.item import Item, RequestItem
from app.interfaces.repository import IRepository


class ItemManager:
    @staticmethod
    def get_items(repository: IRepository, category: str) -> list[Item]:
        return repository.get_items(category=category)

    @staticmethod
    def create_item(
        repository: IRepository, category: str, request_item: RequestItem
    ) -> Item:
        insert_result = repository.create_item(category=category, item=request_item)
        return repository.get_item_by_id(
            category=category, item_id=insert_result.inserted_id
        )

    @staticmethod
    def delete_item(repository: IRepository, category: str, item_id: str) -> None:
        repository.delete_item(category=category, item_id=item_id)

    @staticmethod
    def create_deposit(
        repository: IRepository, request_deposit: RequestDeposit
    ) -> Deposit:
        insert_result = repository.create_deposit(deposit=request_deposit)
        return repository.get_deposit_by_id(deposit_id=insert_result.inserted_id)

    @staticmethod
    def get_deposits(repository: IRepository) -> list[Deposit]:
        return repository.get_deposits()

    @staticmethod
    def delete_deposit(repository: IRepository, deposit_id: str) -> DeleteResult | None:
        return repository.delete_deposit(deposit_id=deposit_id)
