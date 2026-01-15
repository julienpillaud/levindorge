import uuid

import pytest

from app.domain.entities import Pagination, QueryParams
from app.domain.filters import FilterEntity
from app.infrastructure.repository.articles import ArticleRepository
from tests.factories.articles import ArticleFactory


@pytest.mark.parametrize(
    "total_items, page, limit, expected_count, expected_total_pages",
    [
        pytest.param(12, 1, 10, 10, 2, id="full_first_page"),
        pytest.param(12, 2, 10, 2, 2, id="partial_last_page"),
        pytest.param(12, 3, 10, 0, 2, id="empty_last_page"),
    ],
)
def test_get_all_pagination(
    article_factory: ArticleFactory,
    article_repository: ArticleRepository,
    total_items: int,
    page: int,
    limit: int,
    expected_count: int,
    expected_total_pages: int,
) -> None:
    article_factory.create_many(total_items)

    result = article_repository.get_all(pagination=Pagination(page=page, limit=limit))

    assert result.page == page
    assert result.limit == limit
    assert result.total == total_items
    assert result.total_pages == expected_total_pages
    assert len(result.items) == expected_count


@pytest.mark.parametrize(
    "field_name", ["category", "producer", "product", "distributor"]
)
def test_get_all_search(
    article_factory: ArticleFactory,
    article_repository: ArticleRepository,
    field_name: str,
) -> None:
    result_count = 3
    search_token = str(uuid.uuid4())[:5]
    val_1 = f"Prefix_{search_token}_Suffix"
    val_2 = f"Prefix_{search_token.upper()}"
    val_3 = f"{search_token}_Suffix"
    article_factory.create_one(**{field_name: val_1})
    article_factory.create_one(**{field_name: val_2})
    article_factory.create_one(**{field_name: val_3})
    article_factory.create_many(10, **{field_name: "Incorrect Value"})

    result = article_repository.get_all(query=QueryParams(search=search_token))

    assert len(result.items) == result_count


def test_get_all_filters(
    article_factory: ArticleFactory,
    article_repository: ArticleRepository,
) -> None:
    article_factory.create_many(10)
    article = article_factory.create_one()

    result = article_repository.get_all(
        query=QueryParams(
            filters=[FilterEntity(field="product", value=article.product)]
        )
    )

    assert len(result.items) == 1
