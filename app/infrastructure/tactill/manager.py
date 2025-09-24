from collections.abc import Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar

from tactill import TactillClient
from tactill.entities.catalog.article import ArticleCreation
from tactill.entities.catalog.category import Category
from tactill.entities.catalog.tax import Tax

from app.domain.articles.entities import Article
from app.domain.commons.entities import DisplayGroup
from app.domain.protocols.pos_manager import POSManagerProtocol
from app.domain.shops.entities import Shop
from app.infrastructure.tactill.utils import define_color, define_icon_text, define_name

P = ParamSpec("P")
R = TypeVar("R")


class TactillManagerError(Exception):
    pass


class TactillManager(POSManagerProtocol):
    def __init__(self) -> None:
        self._client: TactillClient | None = None
        self._current_shop: Shop | None = None

    @property
    def client(self) -> TactillClient:
        if self._client is None:
            raise TactillManagerError()
        return self._client

    @client.setter
    def client(self, value: TactillClient) -> None:
        self._client = value

    @staticmethod
    def with_client(
        func: Callable[Concatenate["TactillManager", Shop, P], R],
    ) -> Callable[Concatenate["TactillManager", Shop, P], R]:
        @wraps(func)
        def wrapper(
            self: "TactillManager",
            shop: Shop,
            /,
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> R:
            if self._current_shop != shop or self._client is None:
                self._client = TactillClient(api_key=shop.tactill_api_key)
                self._current_shop = shop

            return func(self, shop, *args, **kwargs)

        return wrapper

    def get_category(self, name: str) -> Category:
        filter_ = f"deprecated=false&is_default=false&name={name}"
        categories = self.client.get_categories(filter=filter_)
        if not categories:
            raise TactillManagerError()

        return categories[0]

    def get_tax(self, tax_rate: float) -> Tax:
        filter_ = f"deprecated=false&tax_rate={tax_rate}"
        taxes = self.client.get_taxes(filter=filter_)
        if not taxes:
            raise TactillManagerError()

        return taxes[0]

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
    def delete_article_by_reference(
        self,
        shop: Shop,
        /,
        reference: str,
    ) -> None:
        filter_ = f"deprecated=false&is_default=false&reference={reference}"
        articles = self.client.get_articles(filter=filter_)
        if not articles:
            raise TactillManagerError()

        article = articles[0]
        self.client.delete_article(article_id=article.id)
