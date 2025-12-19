import datetime
from collections.abc import Callable
from functools import wraps
from typing import Concatenate, Literal, ParamSpec, TypeVar

from tactill import TactillClient
from tactill.entities.catalog.article import Article as TactillArticle
from tactill.entities.catalog.article import ArticleCreation, ArticleModification
from tactill.entities.catalog.category import Category as TactillCategory
from tactill.entities.catalog.tax import Tax
from tactill.entities.stock.movement import ArticleMovement, MovementCreation
from tactill.utils import get_query_filter

from app.domain._shared.protocols.pos_manager import POSManagerProtocol
from app.domain.articles.entities import Article
from app.domain.categories.entities import Category
from app.domain.exceptions import POSManagerError
from app.domain.pos.entities import POSArticle
from app.domain.stores.entities import Store
from app.infrastructure.tactill.utils import (
    CATEGORIES_MAPPING,
    INCLUDED_CATEGORIES,
    define_color,
    define_icon_text,
    define_name,
)

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
        func: Callable[Concatenate[T, Store, P], R],
    ) -> Callable[Concatenate[T, Store, P], R]:
        @wraps(func)
        def wrapper(self: T, store: Store, /, *args: P.args, **kwargs: P.kwargs) -> R:
            self._client = TactillClient(api_key=store.tactill_api_key)
            return func(self, store, *args, **kwargs)

        return wrapper

    def _get_categories(
        self,
        name_or_names: str | list[str],
        query_operator: Literal["in", "nin"] | None = None,
    ) -> list[TactillCategory]:
        if isinstance(name_or_names, str):
            filter_ = f"deprecated=false&is_default=false&name={name_or_names}"
        else:
            if query_operator is None:
                raise POSManagerError(
                    "'query_operator' must be provided for list of names"
                )

            query_filter = get_query_filter(
                field="name",
                values=name_or_names,
                query_operator=query_operator,
            )
            filter_ = f"deprecated=false&is_default=false&{query_filter}"

        return self.client.get_categories(filter=filter_)

    def _get_category(self, name: str) -> TactillCategory:
        categories = self._get_categories(name)
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

    def _get_articles_by_category(
        self,
        category_ids: list[str],
        query_operator: Literal["in", "nin"],
    ) -> list[POSArticle]:
        query_filter = get_query_filter(
            field="category_id",
            values=category_ids,
            query_operator=query_operator,
        )
        articles = self.client.get_articles(
            limit=5000,
            filter=f"deprecated=false&is_default=false&{query_filter}",
        )
        return [POSArticle(**article.model_dump()) for article in articles]

    @with_client
    def get_articles(self, _: Store, /) -> list[POSArticle]:
        categories = self._get_categories(INCLUDED_CATEGORIES, query_operator="in")
        category_ids = [category.id for category in categories]

        return self._get_articles_by_category(category_ids, query_operator="in")

    @with_client
    def create_article(
        self,
        store: Store,
        /,
        article: Article,
        category: Category,
    ) -> POSArticle:
        tactill_category = self._get_category(category.tactill_category)
        tactill_tax = self.get_tax(tax_rate=float(article.vat_rate))

        article_creation = ArticleCreation(
            category_id=tactill_category.id,
            taxes=[tactill_tax.id],
            name=define_name(display_group=category.inventory_group, article=article),
            icon_text=define_icon_text(article=article),
            color=define_color(display_group=category.inventory_group, article=article),
            full_price=article.store_data[store.slug].gross_price,
            barcode=article.barcode,
            reference=article.id,
            in_stock=True,
        )
        result = self.client.create_article(article_creation=article_creation)
        return POSArticle(**result.model_dump())

    @with_client
    def update_article(
        self,
        store: Store,
        /,
        article: Article,
        category: Category,
    ) -> None:
        tactill_article = self.get_article_by_reference(reference=article.id)

        tactill_category = self._get_category(category.tactill_category)
        tactill_tax = self.get_tax(tax_rate=float(article.vat_rate))

        article_modification = ArticleModification(
            category_id=tactill_category.id,
            taxes=[tactill_tax.id],
            name=define_name(display_group=category.inventory_group, article=article),
            icon_text=define_icon_text(article=article),
            color=define_color(display_group=category.inventory_group, article=article),
            full_price=article.store_data[store.slug].gross_price,
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
        store: Store,
        /,
        reference: str,
    ) -> None:
        filter_ = f"deprecated=false&is_default=false&reference={reference}"
        articles = self.client.get_articles(filter=filter_)
        if not articles:
            raise POSManagerError()

        article = articles[0]
        self.client.delete_article(article_id=article.id)

    @with_client
    def reset_stocks_by_category(
        self,
        store: Store,
        /,
        category: str,
    ) -> None:
        category_names = CATEGORIES_MAPPING.get(category)
        if not category_names:
            raise POSManagerError()

        categories = self._get_categories(category_names, query_operator="in")
        categories_mapping = {category.id: category.name for category in categories}
        category_ids = [category.id for category in categories]

        articles = self._get_articles_by_category(
            category_ids=category_ids,
            query_operator="in",
        )

        current_date = datetime.datetime.now(datetime.UTC).isoformat()
        article_movements_out = []
        article_movements_in = []
        for article in articles:
            if article.stock_quantity > 0:
                article_movements_out.append(
                    ArticleMovement(
                        article_id=article.id,
                        article_name=article.name,
                        category_name=categories_mapping[article.category_id],
                        state="done",
                        units=article.stock_quantity,
                        done_on=current_date,
                    )
                )
            if article.stock_quantity < 0:
                article_movements_in.append(
                    ArticleMovement(
                        article_id=article.id,
                        article_name=article.name,
                        category_name=categories_mapping[article.category_id],
                        state="done",
                        units=-article.stock_quantity,
                        done_on=current_date,
                    )
                )

        if article_movements_out:
            self.client.create_movement(
                MovementCreation(
                    validated_by=[],
                    type="out",
                    state="done",
                    movements=article_movements_out,
                )
            )
        if article_movements_in:
            self.client.create_movement(
                MovementCreation(
                    validated_by=[],
                    type="in",
                    state="done",
                    movements=article_movements_in,
                )
            )
