from abc import ABC, abstractmethod
from typing import Any, Mapping

from pymongo.results import (
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)

from app.entities.article import (
    Article,
    ArticleType,
    CreateOrUpdateArticle,
    ExtendedArticle,
)
from app.entities.deposit import Deposit, RequestDeposit
from app.entities.inventory import (
    CreateInventory,
    CreateInventoryRecord,
    Inventory,
    InventoryRecord,
    UpdateInventory,
)
from app.entities.item import Item, RequestItem
from app.entities.shop import Shop
from app.entities.volume import RequestVolume, Volume


class IRepository(ABC):
    # --------------------------------------------------------------------------
    # users
    @abstractmethod
    def get_user_by_email(self, email: str) -> Mapping[str, Any] | None:
        pass

    # --------------------------------------------------------------------------
    # types
    @abstractmethod
    def get_types(self) -> list[ArticleType]:
        pass

    @abstractmethod
    def get_ratio_category(self, list_category: str) -> str:
        pass

    @abstractmethod
    def get_article_type(self, type_name: str) -> ArticleType:
        pass

    @abstractmethod
    def get_article_types_by_list(self, list_category: str) -> list[ArticleType]:
        pass

    @abstractmethod
    def get_article_types_by_lists(
        self, lists_category: list[str]
    ) -> list[ArticleType]:
        pass

    # --------------------------------------------------------------------------
    # catalog
    @abstractmethod
    def get_articles(
        self, filter: dict[str, Any] | None = None, to_validate: bool = False
    ) -> list[Article]:
        pass

    @abstractmethod
    def get_extended_articles(self) -> list[ExtendedArticle]:
        pass

    @abstractmethod
    def get_articles_by_list(self, list_category: str) -> list[Article]:
        pass

    @abstractmethod
    def get_article_by_id(self, article_id: str) -> Article:
        pass

    @abstractmethod
    def create_article(self, article: CreateOrUpdateArticle) -> InsertOneResult:
        pass

    @abstractmethod
    def update_article(
        self, article_id: str, article: CreateOrUpdateArticle
    ) -> UpdateResult:
        pass

    @abstractmethod
    def update_article_stock_quantity(
        self, article_id: str, stock_quantity: int, shop: Shop
    ) -> UpdateResult:
        pass

    @abstractmethod
    def delete_article(self, article_id: str) -> DeleteResult:
        pass

    @abstractmethod
    def validate_article(self, article_id: str) -> UpdateResult:
        pass

    # --------------------------------------------------------------------------
    # shops
    @abstractmethod
    def get_shops(self) -> list[Shop]:
        pass

    @abstractmethod
    def get_user_shops(self, user_shops: list[str]) -> list[Shop]:
        pass

    @abstractmethod
    def get_shop_by_username(self, username: str) -> Shop:
        pass

    # ------------------------------------------------------------------------------
    # items
    @abstractmethod
    def get_items_dict(self, volume_category: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_items(self, category: str) -> list[Item]:
        pass

    @abstractmethod
    def get_item_by_id(self, category: str, item_id: str) -> Item:
        pass

    @abstractmethod
    def create_item(self, category: str, item: RequestItem) -> InsertOneResult:
        pass

    @abstractmethod
    def delete_item(self, category: str, item_id: str) -> DeleteResult | None:
        pass

    @abstractmethod
    def get_volumes_by_category(self, volume_category: str) -> list[Volume]:
        pass

    @abstractmethod
    def get_volumes(self) -> list[Volume]:
        pass

    @abstractmethod
    def create_volume(self, volume: RequestVolume) -> InsertOneResult:
        pass

    @abstractmethod
    def get_volume_by_id(self, volume_id: str) -> Volume:
        pass

    @abstractmethod
    def delete_volume(self, volume_id: str) -> DeleteResult | None:
        pass

    @abstractmethod
    def get_deposits(self) -> list[Deposit]:
        pass

    @abstractmethod
    def get_deposit_by_id(self, deposit_id: str) -> Deposit:
        pass

    @abstractmethod
    def create_deposit(self, deposit: RequestDeposit) -> InsertOneResult:
        pass

    @abstractmethod
    def delete_deposit(self, deposit_id: str) -> DeleteResult | None:
        pass

    # --------------------------------------------------------------------------
    # inventory
    @abstractmethod
    def get_inventories(self) -> list[Inventory]:
        pass

    @abstractmethod
    def get_inventory(self, inventory_id: str) -> Inventory:
        pass

    @abstractmethod
    def create_inventory(self, inventory: CreateInventory) -> InsertOneResult:
        pass

    @abstractmethod
    def update_inventory(
        self, inventory_id: str, inventory: UpdateInventory
    ) -> UpdateResult:
        pass

    @abstractmethod
    def delete_inventory(self, inventory_id: str) -> DeleteResult:
        pass

    @abstractmethod
    def get_inventory_records(self, inventory_id: str) -> list[InventoryRecord]:
        pass

    @abstractmethod
    def save_inventory_records(
        self,
        inventory_records: list[CreateInventoryRecord],
    ) -> InsertManyResult:
        pass

    @abstractmethod
    def delete_inventory_records(self, inventory_id: str) -> DeleteResult:
        pass
