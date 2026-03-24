from typing import Annotated

import typer
from cleanstack.infrastructure.mongo.types import MongoDocument
from rich import print

from app.core.config.settings import Settings
from app.core.context import Context
from app.domain.pos.entities import POSArticle
from app.domain.stores.entities import Store
from scripts.utils import get_context

app = typer.Typer()


@app.command()
def migrate(
    source: Annotated[str, typer.Argument()] = "dashboard",
    destination: Annotated[str, typer.Argument()] = "temp",
) -> None:
    src_settings = Settings(mongo_database=source)
    dst_settings = Settings(mongo_database=destination)
    src_context = get_context(settings=src_settings)
    dst_context = get_context(settings=dst_settings)

    dashboard_articles = get_dashboard_articles(src_context)
    stores = get_stores(dst_context)

    for store in stores:
        tactill_articles = get_tactill_articles(dst_context, store)

        for article_id, dashboard_article in dashboard_articles.items():
            if article_id not in tactill_articles:
                print(f"Article not found: {dashboard_article}")

        for article_reference, tactill_article in tactill_articles.items():
            if article_reference not in dashboard_articles:
                print(f"Article not found: {tactill_article}")


def get_dashboard_articles(context: Context) -> dict[str, MongoDocument]:
    result = context.mongo_context.database["articles"].find().to_list()
    print(f"Dashboard articles: {len(result)}")
    return {str(article["_id"]): article for article in result}


def get_stores(context: Context) -> list[Store]:
    return context.store_repository.get_all().items


def get_tactill_articles(context: Context, store: Store) -> dict[str, POSArticle]:
    articles = context.pos_manager.get_articles(store)
    print(f"{store.name} articles: {len(articles)}")
    return {article.reference: article for article in articles}
