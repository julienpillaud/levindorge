import datetime

from cleanstack.exceptions import NotFoundError

from app.domain.articles.entities import Article, ArticleCreateOrUpdate
from app.domain.commons.entities import DisplayGroup
from app.domain.context import ContextProtocol
from app.domain.entities import PyObjectId
from app.domain.users.entities import User


def get_articles_command(context: ContextProtocol) -> list[Article]:
    return context.repository.get_all_articles()


def get_articles_by_display_group_command(
    context: ContextProtocol,
    display_group: DisplayGroup,
) -> list[Article]:
    return context.repository.get_articles_by_list(display_group=display_group)


def get_article_command(context: ContextProtocol, article_id: str) -> Article:
    return context.repository.get_article(article_id=article_id)


def create_article_command(
    context: ContextProtocol,
    current_user: User,
    data: ArticleCreateOrUpdate,
) -> Article:
    current_time = datetime.datetime.now(datetime.UTC)
    article = Article(
        id="",
        **data.model_dump(),
        validated=False,
        created_by=current_user.name,
        created_at=current_time,
        updated_at=current_time,
    )
    return context.repository.create_article(article=article)


def delete_article_command(context: ContextProtocol, article_id: PyObjectId) -> None:
    article = context.repository.get_article(article_id=article_id)
    if not article:
        raise NotFoundError()

    context.repository.delete_article(article=article)
