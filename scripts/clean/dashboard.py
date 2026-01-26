from bson import ObjectId
from rich import print

from app.core.core import Context
from app.domain.stores.entities import Store
from scripts.clean.entities import ArticleReference, Container


def get_stores(context: Context) -> list[Store]:
    result = list(context.database["shops"].find())
    return [
        Store(
            name=store["name"],
            slug=store["username"],
            tactill_api_key=store["tactill_api_key"],
            pricing_configs={},
        )
        for store in result
    ]


def get_dashboard_articles(
    context: Context,
    names: list[str],
) -> dict[ArticleReference, bool]:
    categories = context.database["types"].find({"tactill_category": {"$in": names}})
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
