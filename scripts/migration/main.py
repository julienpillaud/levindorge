from typing import Annotated

import typer
from rich.console import Console

from app.core.config.settings import Settings
from app.core.core import Context
from scripts.migration.articles import create_articles
from scripts.migration.categories import create_categories
from scripts.migration.deposits import create_deposits
from scripts.migration.distributors import create_distributors
from scripts.migration.inventories import create_inventories
from scripts.migration.origins import create_origins
from scripts.migration.producers import create_producers
from scripts.migration.stores import create_stores
from scripts.migration.volumes import create_volume

app = typer.Typer()
console = Console()


@app.command()
def migrate(
    source: Annotated[str, typer.Argument()] = "dashboard",
    destination: Annotated[str, typer.Argument()] = "temp",
    delete_destination: Annotated[bool, typer.Option("--delete", "-d")] = True,
) -> None:
    src_settings = Settings(mongo_database=source)  # ty:ignore[missing-argument]
    dst_settings = Settings(mongo_database=destination)  # ty:ignore[missing-argument]
    src_context = Context(settings=src_settings)
    dst_context = Context(settings=dst_settings)

    if delete_destination:
        for collection_name in dst_context.database.list_collection_names():
            dst_context.database[collection_name].drop()

    stores = create_stores(src_context=src_context, dst_context=dst_context)
    categories = create_categories(dst_context=dst_context)
    origins = create_origins(dst_context=dst_context)

    articles = create_articles(
        src_context=src_context,
        dst_context=dst_context,
        stores=stores,
        categories=categories,
        origins=origins,
    )

    create_producers(
        dst_context=dst_context,
        articles=articles,
        categories=categories,
    )
    create_distributors(dst_context=dst_context, articles=articles)
    create_volume(
        dst_context=dst_context,
        categories=categories,
        articles=articles,
    )
    create_deposits(
        dst_context=dst_context,
        categories=categories,
        articles=articles,
    )

    create_inventories(
        src_context=src_context,
        dst_context=dst_context,
        stores=stores,
    )


if __name__ == "__main__":
    app()
