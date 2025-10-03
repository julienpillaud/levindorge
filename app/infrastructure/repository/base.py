from typing import Any

from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.database import Database

from app.domain.items.entities import ItemType
from app.domain.protocols.repository import RepositoryProtocol
from app.infrastructure.repository.articles import ArticleRepository
from app.infrastructure.repository.deposits import DepositRepository
from app.infrastructure.repository.inventories import InventoryRepository
from app.infrastructure.repository.items import ItemRepository
from app.infrastructure.repository.shops import ShopRepository
from app.infrastructure.repository.types import ArticleTypeRepository
from app.infrastructure.repository.users import UserRepository
from app.infrastructure.repository.volumes import VolumeRepository


class MongoRepository(
    RepositoryProtocol,
    ShopRepository,
    UserRepository,
    ArticleTypeRepository,
    ArticleRepository,
    ItemRepository,
    VolumeRepository,
    DepositRepository,
    InventoryRepository,
):
    def __init__(self, database: Database[MongoDocument]):
        self.database = database

    def get_items_dict(self, volume_category: str | None) -> dict[str, Any]:
        return {
            "country_list": self.get_items(ItemType.COUNTRIES),
            "region_list": self.get_items(ItemType.REGIONS),
            "brewery_list": self.get_items(ItemType.BREWERIES),
            "distillery_list": self.get_items(ItemType.DISTILLERIES),
            "distributor_list": self.get_items(ItemType.DISTRIBUTORS),
            "volumes": self.get_volumes_by_category(volume_category),
            "deposits": self.get_deposits(),
        }
