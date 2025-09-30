from typing import Any, Protocol

from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.database import Database

from app.domain.articles.entities import Article
from app.domain.commons.entities import ArticleType, DisplayGroup
from app.domain.entities import EntityId
from app.domain.items.entities import Deposit, Item, Volume
from app.domain.shops.entities import Shop
from app.domain.users.entities import User


class BaseRepositoryProtocol(Protocol):
    database: Database[MongoDocument]


class ShopRepositoryProtocol(BaseRepositoryProtocol, Protocol):
    def get_shops(self) -> list[Shop]: ...


class UserRepositoryProtocol(BaseRepositoryProtocol, Protocol):
    def get_user_by_email(self, email: str) -> User | None: ...


class ArticleTypeRepositoryProtocol(BaseRepositoryProtocol, Protocol):
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


class ArticleRepositoryProtocol(BaseRepositoryProtocol, Protocol):
    def get_all_articles(self) -> list[Article]: ...

    def get_articles_by_display_group(
        self,
        display_group: DisplayGroup,
    ) -> list[Article]: ...

    def get_article(self, article_id: EntityId) -> Article | None: ...

    def create_article(self, article: Article) -> Article: ...

    def update_article(self, article: Article) -> Article: ...

    def delete_article(self, article: Article) -> None: ...


class ItemRepositoryProtocol(BaseRepositoryProtocol, Protocol):
    def get_items_dict(self, volume_category: str | None) -> dict[str, Any]: ...

    def get_items(self, name: str) -> list[Item]: ...

    def get_volumes(self) -> list[Volume]: ...

    def get_deposits(self) -> list[Deposit]: ...


class RepositoryProtocol(
    ShopRepositoryProtocol,
    UserRepositoryProtocol,
    ArticleTypeRepositoryProtocol,
    ArticleRepositoryProtocol,
    ItemRepositoryProtocol,
    Protocol,
): ...
