from app.domain.articles.entities import Article
from app.domain.context import ContextProtocol


def get_articles_command(
    context: ContextProtocol,
    list_category: str,
) -> list[Article]:
    return context.repository.get_articles_by_list_category(
        list_category=list_category,
    )
