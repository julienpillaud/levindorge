from collections import defaultdict

from rich import print

from app.domain.stores.entities import Store
from app.infrastructure.tactill.manager import TactillManager
from scripts.clean.entities import ArticleReference, Container, POSArticleContainer


def build_pos_containers(
    stores: list[Store],
    names: list[str],
) -> dict[ArticleReference, list[POSArticleContainer]]:
    pos_container_map = defaultdict(list)
    for store in stores:
        manager = TactillManager()
        articles = manager.get_articles_by_category(store, category_ids=names)

        for article in articles:
            if not article.reference:
                continue
            pos_container_map[article.reference].append(
                POSArticleContainer(
                    manager=manager,
                    article_id=article.id,
                    name=article.name or "",
                    stock_quantity=article.stock_quantity,
                )
            )

    return pos_container_map


def delete_pos_articles(containers: list[Container]) -> None:
    to_delete = [
        container for container in containers if container.pos and container.empty_stock
    ]
    print(f"Tactill articles to delete: {len(to_delete)}")
    if not to_delete:
        return


#
#     for container in to_delete:
#         for pos in container.pos:
#             delete_article(container=pos)
#
#
# def delete_article(container: POSArticleContainer) -> None:
#     container.client.delete_article(article_id=container.article_id)
