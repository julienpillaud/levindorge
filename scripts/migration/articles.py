import datetime
from decimal import Decimal
from typing import Any

from rich import print

from app.core.core import Context
from app.domain.articles.entities import (
    Article,
    ArticleDeposit,
    ArticleStoreData,
    ArticleVolume,
)
from app.domain.articles.utils import compute_article_margins, compute_recommended_price
from app.domain.categories.entities import Category
from app.domain.commons.category_groups import CATEGORY_GROUPS_MAP, CategoryGroup
from app.domain.commons.entities import PricingGroup
from app.domain.origins.entities import Origin
from app.domain.stores.entities import Store
from app.domain.types import StoreSlug

NON_MATCH_ORIGINS_MAP = {
    "Ecosse": "Écosse",
    "Etats-Unis": "États-Unis",
    "Corée": "Corée du Sud",
    "République tchèque": "Tchéquie",
}


def create_articles(
    src_context: Context,
    dst_context: Context,
    stores: list[Store],
    categories: list[Category],
    origins: list[Origin],
) -> list[Article]:
    # Get previous articles
    src_articles = list(src_context.database["articles"].find())
    # Create articles with the new entity model
    dst_articles = create_article_entities(
        src_articles=src_articles,
        categories=categories,
        stores=stores,
        origins=origins,
    )
    # Save articles in the database
    result = dst_context.article_repository.create_many(dst_articles)
    count = len(result)
    print(f"Created {count} articles ({len(src_articles)})")
    return dst_context.article_repository.get_all(limit=count).items


def create_article_entities(
    src_articles: list[dict[str, Any]],
    categories: list[Category],
    stores: list[Store],
    origins: list[Origin],
) -> list[Article]:
    categories_map = {category.name: category for category in categories}
    pricing_groups_map = {
        category.name: category.pricing_group for category in categories
    }
    origins_map = {origin.name: origin for origin in origins}

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
            category=article["type"],
            producer=producer,
            product=product,
            cost_price=to_decimal(article["buy_price"]),
            excise_duty=to_decimal(article["excise_duty"]),
            social_security_contribution=to_decimal(article["social_security_levy"]),
            vat_rate=to_decimal(article["tax"]),
            distributor=article["distributor"],
            barcode=article["barcode"],
            origin=get_origin(value=article["region"], origins_map=origins_map),
            color=empty_to_none(article["color"]),
            taste=empty_to_none(article["taste"]),
            volume=get_volume(article=article),
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


def get_origin(value: str, origins_map: dict[str, Origin]) -> str | None:
    if not value:
        return None

    origin = origins_map.get(value)
    if origin:
        return origin.name

    origin_name = NON_MATCH_ORIGINS_MAP.get(value)
    if origin_name:
        return origin_name

    print(f"[bold red]No origin found for {value}[/bold red]")
    return value


def empty_to_none(value: Any) -> str | None:
    return value or None


def convert_volume(value: float, unit: str) -> tuple[float, str]:
    if unit == "cL" and value >= 100:  # noqa: PLR2004
        value /= 100
        unit = "L"
    return value, unit


def get_volume(article: dict[str, Any]) -> ArticleVolume | None:
    if not article["volume"]:
        return None

    volume_value, volume_unit = convert_volume(
        value=article["volume"]["value"],
        unit=article["volume"]["unit"],
    )
    return ArticleVolume(value=volume_value, unit=volume_unit)


def get_deposit(
    article: dict[str, Any],
    /,
    category_group: CategoryGroup,
) -> ArticleDeposit | None:
    if not category_group.deposit:
        return None

    unit = article["deposit"]["unit"]
    if not unit:
        return None

    return ArticleDeposit(
        unit=unit,
        case=article["deposit"]["case"] or None,
        packaging=article["packaging"] or None,
    )


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
