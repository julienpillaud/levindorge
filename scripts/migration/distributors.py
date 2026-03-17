import uuid

from rich import print

from app.core.context import Context
from app.domain.articles.entities import Article
from app.domain.distributors.entities import Distributor


def create_distributors(dst_context: Context, articles: list[Article]) -> None:
    # Create distributors with the new entity model
    dst_distributors = create_producer_entities(articles=articles)

    # Save distributors in the database
    result = dst_context.distributor_repository.create_many(dst_distributors)

    count = len(result)
    print(f"Created {count} distributors")


def create_producer_entities(articles: list[Article]) -> list[Distributor]:
    dst_distributors: dict[str, Distributor] = {}
    for article in articles:
        if not article.distributor:
            continue

        if article.distributor not in dst_distributors:
            dst_distributors[article.distributor] = Distributor(
                id=uuid.uuid7(),
                name=article.distributor,
            )

    return list(dst_distributors.values())
