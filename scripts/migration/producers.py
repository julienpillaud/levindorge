from rich import print

from app.core.core import Context
from app.domain.articles.entities import Article
from app.domain.categories.entities import Category
from app.domain.commons.category_groups import CATEGORY_GROUPS_MAP
from app.domain.producers.entities import Producer


def create_producers(
    dst_context: Context,
    articles: list[Article],
    categories: list[Category],
) -> None:
    # Create producers with the new entity model
    dst_producers = create_producer_entities(
        articles=articles,
        categories=categories,
    )
    # Save producers in the database
    result = dst_context.producer_repository.create_many(dst_producers)
    count = len(result)
    print(f"Created {count} producers")


def create_producer_entities(
    articles: list[Article],
    categories: list[Category],
) -> list[Producer]:
    categories_map = {category.name: category for category in categories}

    dst_producers: list[Producer] = []
    for article in articles:
        if not article.producer:
            continue

        category = categories_map[article.category]
        category_group = CATEGORY_GROUPS_MAP[category.category_group]
        if not category_group.producer:
            continue
        if not category_group.producer.type:
            continue

        producer = Producer(
            name=article.producer,
            type=category_group.producer.type,
        )
        if producer not in dst_producers:
            dst_producers.append(producer)

    return dst_producers
