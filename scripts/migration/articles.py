from typing import Any

from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.database import Database

from app.core.core import Context
from app.domain.articles.entities import Article
from app.domain.articles.utils import compute_article_margins, compute_recommended_price
from app.domain.commons.entities import PricingGroup
from app.domain.stores.entities import Store


def update_articles(
    src_database: Database[MongoDocument],
    dst_database: Database[MongoDocument],
    dst_context: Context,
) -> None:
    stores = dst_context.store_repository.get_all()
    categories = dst_context.category_repository.get_all()
    pricing_groups_map = {
        category.name: category.pricing_group for category in categories.items
    }

    for src_article in src_database["articles"].find():
        for store in stores.items:
            update_recommended_price(
                article=src_article,
                pricing_groups_map=pricing_groups_map,
                store=store,
            )
            update_article_margins(
                article=src_article,
                store=store,
            )

        dst_article = Article(
            category=src_article["type"],
            name=src_article["name"],
            cost_price=src_article["buy_price"],
            excise_duty=src_article["excise_duty"],
            social_security_contribution=src_article["social_security_levy"],
            vat_rate=src_article["tax"],
            distributor=src_article["distributor"],
            barcode=src_article["barcode"],
            region=src_article["region"],
            color=src_article["color"],
            taste=src_article["taste"],
            volume=src_article["volume"],
            alcohol_by_volume=src_article["alcohol_by_volume"],
            packaging=src_article["packaging"],
            deposit=src_article["deposit"],
            created_at=src_article["created_at"],
            updated_at=src_article["updated_at"],
        )
        dst_database.insert_one(dst_article)


def update_recommended_price(
    article: dict[str, Any],
    pricing_groups_map: dict[str, PricingGroup],
    store: Store,
) -> None:
    pricing_group = pricing_groups_map[article["type"]]
    recommended_price = compute_recommended_price(
        total_cost=compute_total_cost(article),
        vat_rate=article["tax"],
        pricing_group=pricing_group,
        pricing_config=store.pricing_configs[pricing_group],
    )
    article["shops"][store.slug]["recommended_price"] = recommended_price


def update_article_margins(
    article: dict[str, Any],
    store: Store,
) -> None:
    margins = compute_article_margins(
        total_cost=compute_total_cost(article),
        tax_rate=article["tax"],
        gross_price=article["shops"][store.slug]["sell_price"],
    )
    article["shops"][store.slug]["margins"] = {
        "margin": margins.margin_amount,
        "markup": margins.margin_rate,
    }


def compute_total_cost(article: dict[str, Any]) -> float:
    total_cost: float = sum(
        [
            article["buy_price"],
            article["excise_duty"],
            article["social_security_levy"],
        ]
    )
    return round(total_cost, 4)
