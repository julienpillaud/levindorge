from typing import Any

from pymongo.database import Database

from app.domain._shared.protocols.repository import RepositoryProtocol
from app.domain.items.entities import ItemType
from app.infrastructure.repository.deposits import DepositRepository
from app.infrastructure.repository.inventories import InventoryRepository
from app.infrastructure.repository.items import ItemRepository
from app.infrastructure.repository.mongo_repository import MongoDocument
from app.infrastructure.repository.types import ArticleTypeRepository


class MongoRepository(
    RepositoryProtocol,
    ArticleTypeRepository,
    ItemRepository,
    DepositRepository,
    InventoryRepository,
):
    def __init__(self, database: Database[MongoDocument]):
        self.database = database

    def get_items_dict(self, volume_category: str | None) -> dict[str, Any]:
        return {
            "distributor_list": self.get_items(ItemType.DISTRIBUTORS),
            "deposits": self.get_deposits(),
        }
