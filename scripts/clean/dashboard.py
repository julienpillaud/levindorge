from typing import Any

from bson import ObjectId
from rich import print

from app.core.core import Context
from scripts.clean.entities import ArticleReference, Container


def get_stores(context: Context) -> list[dict[str, Any]]:
    return list(context.database["shops"].find())


def get_dashboard_articles(
    context: Context,
    name_or_names: str | list[str],
) -> dict[ArticleReference, bool]:
    category_names = (
        [name_or_names] if isinstance(name_or_names, str) else name_or_names
    )
    categories = context.database["types"].find(
        {"tactill_category": {"$in": category_names}}
    )
    type_names = [x["name"] for x in categories]
    articles = context.database["articles"].find({"type": {"$in": type_names}})
    return {str(article["_id"]): True for article in articles}


def delete_dashboard_articles(context: Context, containers: list[Container]) -> None:
    to_delete = [
        ObjectId(container.reference)
        for container in containers
        if container.in_dashboard and container.empty_stock
    ]
    print(f"Dashboard articles to delete: {len(to_delete)}")
    if not to_delete:
        return

    context.database["articles"].delete_many({"_id": {"$in": to_delete}})
