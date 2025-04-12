from app.domain.articles.entities import Article
from app.domain.articles.utils import compute_article_margin, compute_recommended_price
from app.domain.context import ContextProtocol
from app.domain.shops.entities import Shop


def get_articles_command(
    context: ContextProtocol,
    current_shop: Shop,
    list_category: str,
) -> list[Article]:
    articles = context.repository.get_articles_by_list_category(
        list_category=list_category,
    )

    for article in articles:
        article.recommended_price = compute_recommended_price(
            article=article,
            shop=current_shop,
        )
        article.margin = compute_article_margin(
            article=article,
            shop=current_shop,
        )

    return articles
