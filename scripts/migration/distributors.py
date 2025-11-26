from rich import print

from app.core.core import Context
from app.domain.articles.entities import Article
from app.domain.distributors.entities import Distributor


def create_distributors(dst_context: Context, articles: list[Article]) -> None:
    dst_distributors = create_producer_entities(articles=articles)
    result = dst_context.distributor_repository.create_many(dst_distributors)
    count = len(result)
    print(f"Created {count} distributors")


def create_producer_entities(articles: list[Article]) -> list[Distributor]:
    dst_distributors: list[Distributor] = []
    for article in articles:
        if not article.distributor:
            continue

        distributor = Distributor(name=article.distributor)
        if distributor not in dst_distributors:
            dst_distributors.append(distributor)

    return dst_distributors
