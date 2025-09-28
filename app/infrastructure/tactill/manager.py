from collections.abc import Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar

from tactill import TactillClient
from tactill.entities.catalog.article import Article as TactillArticle
from tactill.entities.catalog.article import ArticleCreation, ArticleModification
from tactill.entities.catalog.category import Category
from tactill.entities.catalog.tax import Tax

from app.domain.articles.entities import Article
from app.domain.commons.entities import DisplayGroup
from app.domain.exceptions import POSManagerError
from app.domain.protocols.pos_manager import POSManagerProtocol
from app.domain.shops.entities import Shop
from app.infrastructure.tactill.utils import define_color, define_icon_text, define_name

T = TypeVar("T", bound="TactillManager")
P = ParamSpec("P")
R = TypeVar("R")


class TactillManager(POSManagerProtocol):
    def __init__(self) -> None:
        self._client: TactillClient | None = None

    @property
    def client(self) -> TactillClient:
        if self._client is None:
            raise POSManagerError()
        return self._client

    @staticmethod
    def with_client(
        func: Callable[Concatenate[T, Shop, P], R],
    ) -> Callable[Concatenate[T, Shop, P], R]:
        @wraps(func)
        def wrapper(self: T, shop: Shop, /, *args: P.args, **kwargs: P.kwargs) -> R:
            self._client = TactillClient(api_key=shop.tactill_api_key)
            return func(self, shop, *args, **kwargs)

        return wrapper

    def get_category(self, name: str) -> Category:
        filter_ = f"deprecated=false&is_default=false&name={name}"
        categories = self.client.get_categories(filter=filter_)
        if not categories:
            raise POSManagerError()

        return categories[0]

    def get_tax(self, tax_rate: float) -> Tax:
        filter_ = f"deprecated=false&rate={tax_rate}"
        taxes = self.client.get_taxes(filter=filter_)
        if not taxes:
            raise POSManagerError()

        return taxes[0]

    def get_article_by_reference(self, reference: str) -> TactillArticle:
        filter_ = f"deprecated=false&is_default=false&reference={reference}"
        articles = self.client.get_articles(filter=filter_)
        if not articles:
            raise POSManagerError()

        return articles[0]

    @with_client
    def create_article(
        self,
        shop: Shop,
        /,
        article: Article,
        category_name: str,
        display_group: DisplayGroup,
    ) -> None:
        tactill_category = self.get_category(name=category_name)
        tactill_tax = self.get_tax(tax_rate=article.tax)

        article_creation = ArticleCreation(
            category_id=tactill_category.id,
            taxes=[tactill_tax.id],
            name=define_name(display_group=display_group, article=article),
            icon_text=define_icon_text(article=article),
            color=define_color(display_group=display_group, article=article),
            full_price=article.shops[shop.username].sell_price,
            barcode=article.barcode,
            reference=article.id,
            in_stock=True,
        )
        self.client.create_article(article_creation=article_creation)

    @with_client
    def update_article(
        self,
        shop: Shop,
        /,
        article: Article,
        category_name: str,
        display_group: DisplayGroup,
    ) -> None:
        tactill_article = self.get_article_by_reference(reference=article.id)

        tactill_category = self.get_category(name=category_name)
        tactill_tax = self.get_tax(tax_rate=article.tax)

        article_modification = ArticleModification(
            category_id=tactill_category.id,
            taxes=[tactill_tax.id],
            name=define_name(display_group=display_group, article=article),
            icon_text=define_icon_text(article=article),
            color=define_color(display_group=display_group, article=article),
            full_price=article.shops[shop.username].sell_price,
            barcode=article.barcode,
            in_stock=True,
        )
        self.client.update_article(
            article_id=tactill_article.id,
            article_modification=article_modification,
        )

    @with_client
    def delete_article_by_reference(
        self,
        shop: Shop,
        /,
        reference: str,
    ) -> None:
        filter_ = f"deprecated=false&is_default=false&reference={reference}"
        articles = self.client.get_articles(filter=filter_)
        if not articles:
            raise POSManagerError()

        article = articles[0]
        self.client.delete_article(article_id=article.id)
