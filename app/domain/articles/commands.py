import datetime

from app.domain.articles.entities import (
    Article,
    ArticleCreateOrUpdate,
    ArticleToDb,
    AugmentedArticle,
)
from app.domain.articles.utils import compute_article_margins, compute_recommended_price
from app.domain.context import ContextProtocol
from app.domain.shops.entities import Shop
from app.domain.users.entities import User


def get_articles_command(
    context: ContextProtocol,
    current_shop: Shop,
    list_category: str,
) -> list[AugmentedArticle]:
    articles = context.repository.get_articles_by_list_category(
        list_category=list_category,
    )

    augmented_articles: list[AugmentedArticle] = []
    for article in articles:
        recommended_price = compute_recommended_price(
            ratio_category=article.type_infos.ratio_category,
            taxfree_price=article.taxfree_price,
            tax=article.tax,
            shop=current_shop,
        )
        margin = compute_article_margins(
            taxfree_price=article.taxfree_price,
            tax=article.tax,
            sell_price=article.shops[current_shop.username].sell_price,
        )
        augmented_article = AugmentedArticle(
            **article.model_dump(),
            recommended_price=recommended_price,
            margin=margin,
        )
        augmented_articles.append(augmented_article)

    return augmented_articles


def get_article_command(context: ContextProtocol, article_id: str) -> Article:
    return context.repository.get_article_by_id(article_id=article_id)


def create_article_command(
    context: ContextProtocol,
    current_user: User,
    data: ArticleCreateOrUpdate,
) -> Article:
    current_time = datetime.datetime.now(datetime.UTC)
    article = ArticleToDb(
        **data.model_dump(),
        created_by=current_user.name,
        created_at=current_time,
        updated_at=current_time,
    )

    return context.repository.create_article(article=article)


def update_article_command(
    context: ContextProtocol,
    current_user: User,
    article_id: str,
    data: ArticleCreateOrUpdate,
) -> Article:
    existing_article = context.repository.get_article_by_id(article_id=article_id)

    current_time = datetime.datetime.now(datetime.UTC)
    article = Article(
        id=existing_article.id,
        **data.model_dump(),
        created_by=current_user.name,
        created_at=existing_article.created_at,
        updated_at=current_time,
        type_infos=existing_article.type_infos,
    )

    return context.repository.update_article(article=article)


def delete_article_command(context: ContextProtocol, article_id: str) -> None:
    existing_article = context.repository.get_article_by_id(article_id=article_id)
    context.repository.delete_article(article=existing_article)
