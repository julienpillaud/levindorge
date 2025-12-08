from collections import defaultdict
from typing import Any

from rich import print
from tactill import TactillClient
from tactill.entities.catalog.article import Article

from app.infrastructure.tactill.tactill import get_articles_by_category, get_categories
from scripts.clean.entities import ArticleReference, Container, POSArticleContainer


def build_pos_containers(
    stores: list[dict[str, Any]],
    name_or_names: str | list[str],
) -> dict[ArticleReference, list[POSArticleContainer]]:
    pos_container_map = defaultdict(list)
    for store in stores:
        client = TactillClient(api_key=store["tactill_api_key"])
        articles = get_articles(client=client, name_or_names=name_or_names)

        for article in articles:
            if not article.reference:
                continue
            pos_container_map[article.reference].append(
                POSArticleContainer(
                    client=client,
                    article_id=article.id,
                    name=article.name,
                    stock_quantity=article.stock_quantity,
                )
            )

    return pos_container_map


def get_articles(
    client: TactillClient,
    name_or_names: str | list[str],
) -> list[Article]:
    categories = get_categories(client, name_or_names, query_operator="in")
    category_ids = [category.id for category in categories]
    return get_articles_by_category(client, category_ids, query_operator="in")


def delete_pos_articles(containers: list[Container]) -> None:
    to_delete = [
        container for container in containers if container.pos and container.empty_stock
    ]
    print(f"Tactill articles to delete: {len(to_delete)}")
    if not to_delete:
        return

    for container in to_delete:
        for pos in container.pos:
            delete_article(container=pos)


def delete_article(container: POSArticleContainer) -> None:
    container.client.delete_article(article_id=container.article_id)
