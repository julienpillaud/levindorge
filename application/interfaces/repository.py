from abc import ABC, abstractmethod
from typing import Any, Mapping

from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from application.entities.article import (
    Article,
    ArticleType,
    CreateOrUpdateArticle,
    InventoryArticle,
)
from application.entities.inventory import CreateOrUpdateInventory, Inventory
from application.entities.item import Item, RequestItem
from application.entities.shop import Shop


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
    def get_items_dict(self, list_category: str) -> dict[str, Any]:
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
    def delete_item(self, category: str, item_id: str) -> DeleteResult:
        pass

    # --------------------------------------------------------------------------
    # inventory
    @abstractmethod
    def get_inventory_record(self, article_id: str) -> Inventory:
        pass

    @abstractmethod
    def save_inventory_record(
        self,
        inventory_record: CreateOrUpdateInventory,
    ) -> UpdateResult:
        pass

    @abstractmethod
    def reset_inventory(self) -> DeleteResult:
        pass

    @abstractmethod
    def get_articles_inventory(self, match: dict[str, Any]) -> list[InventoryArticle]:
        pass

    @abstractmethod
    def get_articles_for_inventory(self) -> dict[str, list[InventoryArticle]]:
        pass
