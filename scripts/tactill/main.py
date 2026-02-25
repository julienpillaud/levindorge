from typing import Annotated

import typer
from rich import print

from app.core.config.settings import Settings
from app.domain.domain import Domain
from scripts.utils import get_context

app = typer.Typer()


@app.command()
def migrate(database: Annotated[str, typer.Argument()] = "temp") -> None:
    settings = Settings(mongo_database=database)
    context = get_context(settings=settings)
    domain = Domain(uow=context.uow, context=context)

    articles = domain.get_articles(limit=3000)
    print(f"Dashboard articles: {len(articles.items)}\n")
    articles_map = {article.id: article for article in articles.items}

    articles_not_found = {}
    stores = context.store_repository.get_all()
    for store in stores.items:
        tactill_articles = context.pos_manager.get_articles(store)
        print(f"\n{store.name} articles: {len(tactill_articles)}\n")
        tactill_articles_map = {
            article.reference: article for article in tactill_articles
        }

        for article in articles.items:
            if article.id not in tactill_articles_map:
                print(f"Article not found: {article.display_name}")

        for article in tactill_articles:
            if (
                article.reference not in articles_map
                and article.reference not in articles_not_found
            ):
                articles_not_found[article.reference] = article

    print(f"\nArticles not found: {len(articles_not_found)}\n")
    for article in articles_not_found.values():
        print(article)
