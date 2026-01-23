from typing import Annotated

import typer
from rich import print

from app.core.config.settings import Settings
from app.core.core import Context
from app.domain.domain import Domain

app = typer.Typer()


@app.command()
def migrate(database: Annotated[str, typer.Argument()] = "temp") -> None:
    settings = Settings(mongo_database=database)  # ty:ignore[missing-argument]
    context = Context(settings=settings)
    domain = Domain(context=context)

    articles = domain.get_articles(limit=3000)
    print(f"Dashboard articles: {len(articles.items)}\n")

    stores = context.store_repository.get_all()
    for store in stores.items:
        tactill_articles = context.pos_manager.get_articles(store)
        print(f"{store.name} articles: {len(tactill_articles)}\n")
        tactill_articles_map = {
            article.reference: article for article in tactill_articles
        }

        for article in articles.items:
            if article.id not in tactill_articles_map:
                print(f"Article not found: {article.display_name}")
