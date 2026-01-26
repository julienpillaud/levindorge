import datetime
from collections.abc import Callable
from functools import wraps
from typing import Concatenate, Literal, ParamSpec, TypeVar

import logfire
from tactill import FilterEntity, FilterOperator, QueryParams, TactillClient
from tactill.entities import Article as TactillArticle
from tactill.entities import ArticleCreation, ArticleModification, Tax
from tactill.entities import Category as TactillCategory
from tactill.entities.stock.movement import ArticleMovement, MovementCreation

from app.domain.articles.entities import Article
from app.domain.categories.entities import Category
from app.domain.exceptions import POSManagerError
from app.domain.pos.entities import POSArticle
from app.domain.protocols.pos_manager import POSManagerProtocol
from app.domain.stores.entities import Store
from app.infrastructure.tactill.utils import (
    CATEGORIES_MAPPING,
    INCLUDED_CATEGORIES,
    define_color,
    define_icon_text,
    define_name,
)
from data.categories import CATEGORY_MAPPING

T = TypeVar("T", bound="TactillManager")
P = ParamSpec("P")
R = TypeVar("R")


class TactillManager(POSManagerProtocol):
    def __init__(self) -> None:
        self._api_key: str | None = None
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
            if store.tactill_api_key != self._api_key:
                self._api_key = store.tactill_api_key
                self._client = TactillClient(api_key=store.tactill_api_key)
            return func(self, store, *args, **kwargs)

        return wrapper

    def _get_categories_by_name(
        self,
        names: list[str],
        /,
        operator: Literal[FilterOperator.IN, FilterOperator.NIN] = FilterOperator.IN,
    ) -> list[TactillCategory]:
        query = QueryParams(
            filters=[
                FilterEntity(field="deprecated", value="false"),
                FilterEntity(field="is_default", value="false"),
                FilterEntity(field="name", value=names, operator=operator),
            ],
        )
        return self.client.get_categories(query=query)

    def _get_category(self, name: str) -> TactillCategory:
        categories = self._get_categories_by_name([name])
        if not categories:
            raise POSManagerError(f"Category '{name}' not found.")

        return categories[0]

    def _get_tax(self, tax_rate: float) -> Tax:
        query = QueryParams(
            limit=1,
            filters=[
                FilterEntity(field="deprecated", value="false"),
                FilterEntity(field="rate", value=tax_rate),
            ],
        )
        taxes = self.client.get_taxes(query=query)
        if not taxes:
            raise POSManagerError(f"Tax rate '{tax_rate}' not found.")

        return taxes[0]

    def _get_article_by_reference(self, article: Article) -> TactillArticle:
        query = QueryParams(
            limit=1,
            filters=[
                FilterEntity(field="deprecated", value="false"),
                FilterEntity(field="is_default", value="false"),
                FilterEntity(field="reference", value=article.reference.hex),
            ],
        )
        articles = self.client.get_articles(query=query)
        if not articles:
            logfire.info(
                f"Article '{article.id}' not found.",
                extra=article.model_dump(),
            )
            raise POSManagerError(f"Article '{article.id}' not found.")

        return articles[0]

    @with_client
    def get_articles_by_category(
        self,
        store: Store,
        /,
        category_ids: list[str],
        operator: Literal[FilterOperator.IN, FilterOperator.NIN] = FilterOperator.IN,
    ) -> list[POSArticle]:
        query = QueryParams(
            limit=5000,
            filters=[
                FilterEntity(field="deprecated", value="false"),
                FilterEntity(field="is_default", value="false"),
                FilterEntity(
                    field="category_id", value=category_ids, operator=operator
                ),
            ],
        )
        articles = self.client.get_articles(query=query)
        return [POSArticle(**article.model_dump()) for article in articles]

    @with_client
    def get_articles(self, store: Store, /) -> list[POSArticle]:
        categories = self._get_categories_by_name(INCLUDED_CATEGORIES)
        category_ids = [category.id for category in categories]
        return self.get_articles_by_category(store, category_ids=category_ids)

    @with_client
    def create_article(
        self,
        store: Store,
        /,
        article: Article,
        category: Category,
    ) -> POSArticle:
        tactill_category = self._get_category(CATEGORY_MAPPING[category.name])
        tactill_tax = self._get_tax(tax_rate=float(article.vat_rate))

        article_creation = ArticleCreation(
            category_id=tactill_category.id,
            taxes=[tactill_tax.id],
            name=define_name(display_group=category.inventory_group, article=article),
            icon_text=define_icon_text(article=article),
            color=define_color(display_group=category.inventory_group, article=article),
            full_price=float(article.store_data[store.slug].gross_price),
            barcode=article.barcode,
            reference=article.reference.hex,
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
        tactill_article = self._get_article_by_reference(article=article)
        tactill_category = self._get_category(CATEGORY_MAPPING[category.name])
        tactill_tax = self._get_tax(tax_rate=float(article.vat_rate))

        article_modification = ArticleModification(
            category_id=tactill_category.id,
            taxes=[tactill_tax.id],
            name=define_name(display_group=category.inventory_group, article=article),
            icon_text=define_icon_text(article=article),
            color=define_color(display_group=category.inventory_group, article=article),
            full_price=float(article.store_data[store.slug].gross_price),
            barcode=article.barcode,
            in_stock=True,
        )
        self.client.update_article(
            article_id=tactill_article.id,
            article_modification=article_modification,
        )

    @with_client
    def delete_article(
        self,
        store: Store,
        /,
        article: Article,
    ) -> None:
        tactill_article = self._get_article_by_reference(article=article)
        self.client.delete_article(article_id=tactill_article.id)

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

        categories = self._get_categories_by_name(category_names)
        categories_mapping = {category.id: category.name for category in categories}
        category_ids = [category.id for category in categories]

        articles = self.get_articles_by_category(store, category_ids=category_ids)

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
