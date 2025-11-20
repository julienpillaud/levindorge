from decimal import Decimal
from typing import Any

from app.core.core import Context
from app.domain.articles.entities import Article, ArticleStoreData
from app.domain.articles.utils import compute_article_margins, compute_recommended_price
from app.domain.commons.entities import PricingGroup
from app.domain.stores.entities import Store, StoreSlug


def update_articles(src_context: Context, dst_context: Context) -> None:
    stores = dst_context.store_repository.get_all()
    categories = dst_context.category_repository.get_all()
    pricing_groups_map = {
        category.name: category.pricing_group for category in categories.items
    }

    src_articles = src_context.database["articles"].find()
    dst_articles: list[Article] = []
    for article in src_articles:
        dst_article = Article(
            category=article["type"],
            name=article["name"],
            cost_price=to_decimal(article["buy_price"]),
            excise_duty=to_decimal(article["excise_duty"]),
            social_security_contribution=to_decimal(article["social_security_levy"]),
            vat_rate=to_decimal(article["tax"]),
            distributor=article["distributor"],
            barcode=article["barcode"],
            region=article["region"],
            color=article["color"],
            taste=article["taste"],
            volume=article["volume"],
            alcohol_by_volume=article["alcohol_by_volume"],
            packaging=article["packaging"],
            deposit=article["deposit"],
            created_at=article["created_at"],
            updated_at=article["updated_at"],
            store_data=get_store_data(
                article=article,
                pricing_groups_map=pricing_groups_map,
                stores=stores.items,
            ),
        )
        dst_articles.append(dst_article)

    dst_context.article_repository.create_many(dst_articles)


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
            stock_quantity=article["shops"][store.slug]["stock_quantity"],
            recommended_price=compute_recommended_price(
                total_cost=total_cost,
                vat_rate=to_decimal(article["tax"]),
                pricing_group=pricing_group,
                pricing_config=store.pricing_configs[pricing_group],
            ),
            margins=compute_article_margins(
                total_cost=total_cost,
                tax_rate=to_decimal(article["tax"]),
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
