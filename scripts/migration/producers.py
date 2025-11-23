from app.core.core import Context
from app.domain.producers.entities import Producer
from scripts.migration.categories import CATEGORIES


def update_producers(dst_context: Context) -> None:
    articles = dst_context.article_repository.get_all(limit=3000)
    categories_map = {
        category.name: category for category in CATEGORIES if category.producer_type
    }
    producers: list[Producer] = []
    seen_names: set[str] = set()
    for article in articles.items:
        if not article.producer:
            continue

        if article.producer in seen_names:
            continue

        category = categories_map.get(article.category)
        if not category:
            continue

        seen_names.add(article.producer)
        producers.append(
            Producer(
                name=article.producer,
                type=category.producer_type,
            )
        )

    dst_context.producer_repository.create_many(producers)
