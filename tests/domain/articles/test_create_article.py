import pytest
from cleanstack.exceptions import NotFoundError

from app.domain.articles.commands import create_article_command
from app.domain.articles.entities import ArticleCreateOrUpdate
from app.domain.context import ContextProtocol
from app.domain.stores.entities import Store
from tests.factories.articles import ArticleFactory
from tests.factories.categories import CategoryFactory
from tests.utils import is_str_object_id


def test_create_article(
    context: ContextProtocol,
    store: Store,
    category_factory: CategoryFactory,
    article_factory: ArticleFactory,
) -> None:
    article_data = article_factory.build(stores=[store])
    data = ArticleCreateOrUpdate(**article_data.model_dump())

    article = create_article_command(context, data=data)

    assert is_str_object_id(article.id)
    assert article.reference == data.reference
    assert article.category == data.category
    assert article.producer == data.producer
    assert article.product == data.product
    assert article.cost_price == data.cost_price
    assert article.excise_duty == data.excise_duty
    assert article.social_security_contribution == data.social_security_contribution
    assert article.vat_rate == data.vat_rate
    assert article.distributor == data.distributor
    assert article.barcode == data.barcode
    assert article.origin == data.origin
    assert article.color == data.color
    assert article.taste == data.taste
    assert article.volume == data.volume
    assert article.alcohol_by_volume == data.alcohol_by_volume
    assert article.deposit == data.deposit
    assert article.created_at
    assert article.updated_at
    assert article.store_data == data.store_data


def test_create_article_category_not_found(
    context: ContextProtocol,
    store: Store,
    article_factory: ArticleFactory,
) -> None:
    article_data = article_factory.build(category="category", stores=[store])
    data = ArticleCreateOrUpdate(**article_data.model_dump())

    with pytest.raises(NotFoundError):
        create_article_command(context, data=data)


def test_create_article_store_not_found(
    context: ContextProtocol,
    category_factory: CategoryFactory,
    article_factory: ArticleFactory,
) -> None:
    article_data = article_factory.build()
    data = ArticleCreateOrUpdate(**article_data.model_dump())

    with pytest.raises(NotFoundError):
        create_article_command(context, data=data)
