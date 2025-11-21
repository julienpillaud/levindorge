from app.core.core import Context
from app.domain._shared.entities import ProducerType
from app.domain.articles.entities import Article
from app.domain.producers.entities import Producer
from scripts.migration.categories import CATEGORIES


def update_producers(dst_context: Context) -> None:
    articles = dst_context.article_repository.get_all(limit=3000)
    breweries = [
        Producer(name=name, type=ProducerType.BREWERY)
        for name in get_breweries(articles.items)
    ]
    distilleries = [
        Producer(name=name, type=ProducerType.DISTILLERY)
        for name in get_distilleries(articles.items)
    ]

    dst_context.producer_repository.create_many(breweries + distilleries)


def get_category_names(producer_type: ProducerType) -> list[str]:
    return [
        category.name
        for category in CATEGORIES
        if category.producer_type == producer_type
    ]


def get_breweries(articles: list[Article]) -> list[str]:
    return sorted(
        {
            article.producer
            for article in articles
            if article.category in get_category_names(ProducerType.BREWERY)
            and article.producer
        }
    )


def get_distilleries(articles: list[Article]) -> list[str]:
    return sorted(
        {
            article.producer
            for article in articles
            if article.category in get_category_names(ProducerType.DISTILLERY)
            and article.producer
        }
    )
