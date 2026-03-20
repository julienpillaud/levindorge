import datetime
import uuid
from decimal import Decimal
from typing import Any

from rich import print

from app.core.context import Context
from app.domain.articles.entities import Article, ArticleStoreData
from app.domain.articles.utils import compute_article_margins, compute_recommended_price
from app.domain.categories.entities import Category
from app.domain.commons.category_groups import CATEGORY_GROUPS_MAP, CategoryGroup
from app.domain.commons.entities import PricingGroup
from app.domain.stores.entities import Store
from app.domain.types import StoreSlug
from scripts.migration.articles.deposits import get_deposit
from scripts.migration.articles.origins import get_origin
from scripts.migration.articles.volumes import get_volume


def create_articles(
    src_context: Context,
    dst_context: Context,
    stores: list[Store],
    categories: list[Category],
) -> list[Article]:
    # Get previous articles
    src_articles = src_context.mongo_context.database["articles"].find().to_list()
    # Create articles with the new entity model
    dst_articles = create_article_entities(
        src_articles=src_articles,
        categories=categories,
        stores=stores,
    )

    # Save articles in the database
    result = dst_context.article_repository.create_many(dst_articles)

    count = len(result)
    print(f"Created {count} articles ({len(src_articles)})")

    return dst_articles


def create_article_entities(
    src_articles: list[dict[str, Any]],
    categories: list[Category],
    stores: list[Store],
) -> list[Article]:
    categories_map = {category.name: category for category in categories}
    pricing_groups_map = {
        category.name: category.pricing_group for category in categories
    }

    current_date = datetime.datetime.now(datetime.UTC)
    dst_articles: list[Article] = []
    for article in src_articles:
        category = categories_map[article["type"]]
        category_group = CATEGORY_GROUPS_MAP[category.category_group]

        producer, product = get_producer_and_product(
            article,
            category_group=category_group,
        )
        dst_article = Article(
            id=uuid.uuid7(),
            reference=uuid.uuid7(),
            category=article["type"],
            producer=producer,
            product=product,
            cost_price=to_decimal(article["buy_price"]),
            excise_duty=to_decimal(article["excise_duty"]),
            social_security_contribution=to_decimal(article["social_security_levy"]),
            vat_rate=to_decimal(article["tax"]),
            distributor=article["distributor"],
            barcode=article["barcode"],
            origin=get_origin(article["region"]),
            color=empty_to_none(article["color"]),
            taste=empty_to_none(article["taste"]),
            volume=get_volume(article, category_group=category_group),
            alcohol_by_volume=empty_to_none(article["alcohol_by_volume"]),
            deposit=get_deposit(article, category_group=category_group),
            created_at=current_date,
            updated_at=current_date,
            store_data=get_store_data(
                article=article,
                pricing_groups_map=pricing_groups_map,
                stores=stores,
            ),
        )
        dst_articles.append(dst_article)

    return dst_articles


def get_producer_and_product(
    article: dict[str, Any],
    /,
    category_group: CategoryGroup,
) -> tuple[str | None, str]:
    if category_group.producer:
        if article["name"]["name1"] == "":
            return None, article["name"]["name2"]

        return article["name"]["name1"], article["name"]["name2"]

    return None, article["name"]["name1"]


def empty_to_none(value: Any) -> Any | None:
    return value or None


def get_store_data(
    article: dict[str, Any],
    pricing_groups_map: dict[str, PricingGroup],
    stores: list[Store],
) -> dict[StoreSlug, ArticleStoreData]:
    pricing_group = pricing_groups_map[article["type"]]
    total_cost = compute_total_cost(article)
    return {
        store.slug: ArticleStoreData(
            gross_price=to_decimal(article["shops"][store.slug]["sell_price"]),
            bar_price=to_decimal(article["shops"][store.slug]["bar_price"]),
            stock_quantity=int(article["shops"][store.slug]["stock_quantity"]),
            recommended_price=compute_recommended_price(
                total_cost=total_cost,
                vat_rate=to_decimal(article["tax"]),
                pricing_group=pricing_group,
                pricing_config=store.pricing_configs[pricing_group],
            ),
            margins=compute_article_margins(
                total_cost=total_cost,
                vat_rate=to_decimal(article["tax"]),
                gross_price=to_decimal(article["shops"][store.slug]["sell_price"]),
            ),
        )
        for store in stores
    }


def compute_total_cost(article: dict[str, Any]) -> Decimal:
    return (
        to_decimal(article["buy_price"])
        + to_decimal(article["excise_duty"])
        + to_decimal(article["social_security_levy"])
    )


def to_decimal(value: float) -> Decimal:
    return Decimal(str(value))
