from rich import print

from app.core.core import Context
from app.domain.articles.entities import Article
from app.domain.producers.entities import Producer
from scripts.migration.categories import CATEGORIES


def create_producers(
    dst_context: Context,
    articles: list[Article],
) -> None:
    dst_producers = create_producer_entities(articles=articles)
    result = dst_context.producer_repository.create_many(dst_producers)
    count = len(result)
    print(f"Created {count} producers")


def create_producer_entities(articles: list[Article]) -> list[Producer]:
    categories_map = {
        category.name: category for category in CATEGORIES if category.producer_type
    }

    dst_producers: list[Producer] = []
    seen_names: set[str] = set()
    for article in articles:
        if not article.producer:
            continue

        if article.producer in seen_names:
            continue

        category = categories_map.get(article.category)
        if not category:
            continue

        seen_names.add(article.producer)
        dst_producers.append(
            Producer(
                name=article.producer,
                type=category.producer_type,
            )
        )

    return dst_producers
