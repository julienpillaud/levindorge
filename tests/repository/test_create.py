from app.domain.articles.entities import Article
from app.infrastructure.repository.articles import ArticleRepository
from tests.factories.articles import ArticleFactory
from tests.utils import is_str_object_id


def test_create(
    article_factory: ArticleFactory,
    article_repository: ArticleRepository,
) -> None:
    article = article_factory.build()

    article_db = article_repository.create(article)

    assert is_str_object_id(article_db.id)
    assert isinstance(article_db, Article)
