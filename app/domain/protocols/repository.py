from typing import Any, Protocol

from app.domain.articles.entities import Article
from app.domain.commons.entities import ArticleType, DisplayGroup
from app.domain.deposits.entities import Deposit
from app.domain.entities import EntityId
from app.domain.inventories.entities import Inventory, InventoryRecord, InventoryReport
from app.domain.items.entities import Item, ItemType
from app.domain.shops.entities import Shop
from app.domain.users.entities import User
from app.domain.volumes.entities import Volume


class ShopRepositoryProtocol(Protocol):
    def get_shops(self) -> list[Shop]: ...


class UserRepositoryProtocol(Protocol):
    def get_user(self, user_id: EntityId) -> User | None: ...

    def get_user_by_email(self, email: str) -> User | None: ...

    def update_user(self, user: User) -> User: ...


class ArticleTypeRepositoryProtocol(Protocol):
    def get_article_types(
        self,
        name: str | None = None,
        display_group: DisplayGroup | None = None,
    ) -> list[ArticleType]: ...

    def get_article_type_by_name(self, name: str) -> ArticleType: ...

    def get_article_types_by_list(
        self,
        display_group: DisplayGroup,
    ) -> list[ArticleType]: ...


class ArticleRepositoryProtocol(Protocol):
    def get_articles(self) -> list[Article]: ...

    def get_articles_by_display_group(
        self,
        display_group: DisplayGroup,
    ) -> list[Article]: ...

    def get_article(self, article_id: EntityId) -> Article | None: ...

    def create_article(self, article: Article) -> Article: ...

    def update_article(self, article: Article) -> Article: ...

    def delete_article(self, article: Article) -> None: ...


class ItemRepositoryProtocol(Protocol):
    def get_items(self, item_type: ItemType) -> list[Item]: ...

    def get_item(self, item_type: ItemType, item_id: EntityId) -> Item | None: ...

    def create_item(self, item_type: ItemType, item: Item) -> Item: ...

    def delete_item(self, item_type: ItemType, item: Item) -> None: ...

    def item_is_used(self, item_type: ItemType, item: Item) -> bool: ...


class VolumeRepositoryProtocol(Protocol):
    def get_volumes(self) -> list[Volume]: ...

    def get_volume(self, volume_id: EntityId) -> Volume | None: ...

    def create_volume(self, volume: Volume) -> Volume: ...

    def delete_volume(self, volume: Volume) -> None: ...

    def volume_is_used(self, volume: Volume) -> bool: ...


class DepositRepositoryProtocol(Protocol):
    def get_deposits(self) -> list[Deposit]: ...

    def get_deposit(self, deposit_id: EntityId) -> Deposit | None: ...

    def create_deposit(self, deposit: Deposit) -> Deposit: ...

    def delete_deposit(self, deposit: Deposit) -> None: ...

    def deposit_is_used(self, deposit: Deposit) -> bool: ...


class InventoryRepositoryProtocol(Protocol):
    def get_inventories(self) -> list[Inventory]: ...

    def get_inventory(self, inventory_id: EntityId) -> Inventory | None: ...

    def get_inventory_report(
        self,
        inventory_id: EntityId,
    ) -> InventoryReport | None: ...

    def create_inventory(self, inventory: Inventory) -> Inventory: ...

    def create_inventory_records(
        self,
        inventory_id: EntityId,
        records: list[InventoryRecord],
    ) -> list[InventoryRecord]: ...

    def delete_inventory(self, inventory: Inventory) -> None: ...

    def delete_inventory_records(self, inventory_id: EntityId) -> None: ...


class RepositoryProtocol(
    ShopRepositoryProtocol,
    UserRepositoryProtocol,
    ArticleTypeRepositoryProtocol,
    ArticleRepositoryProtocol,
    ItemRepositoryProtocol,
    VolumeRepositoryProtocol,
    DepositRepositoryProtocol,
    InventoryRepositoryProtocol,
    Protocol,
):
    def get_items_dict(self, volume_category: str | None) -> dict[str, Any]: ...
