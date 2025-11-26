from typing import Literal

from tactill import TactillClient
from tactill.entities.catalog.article import Article
from tactill.entities.catalog.category import Category
from tactill.utils import get_query_filter

from app.domain.exceptions import POSManagerError


def get_categories(
    client: TactillClient,
    name_or_names: str | list[str],
    query_operator: Literal["in", "nin"] | None = None,
) -> list[Category]:
    if isinstance(name_or_names, str):
        filter_ = f"deprecated=false&is_default=false&name={name_or_names}"
    else:
        if query_operator is None:
            raise POSManagerError("'query_operator' must be provided for list of names")

        query_filter = get_query_filter(
            field="name",
            values=name_or_names,
            query_operator=query_operator,
        )
        filter_ = f"deprecated=false&is_default=false&{query_filter}"

    return client.get_categories(filter=filter_)


def get_articles_by_category(
    client: TactillClient,
    category_ids: list[str],
    query_operator: Literal["in", "nin"],
) -> list[Article]:
    query_filter = get_query_filter(
        field="category_id",
        values=category_ids,
        query_operator=query_operator,
    )
    return client.get_articles(
        limit=5000,
        filter=f"deprecated=false&is_default=false&{query_filter}",
    )
