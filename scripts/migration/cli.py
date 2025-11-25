from typing import Annotated

import typer
from rich.console import Console

from app.core.config import Settings
from app.core.core import Context
from scripts.migration.articles import create_articles
from scripts.migration.categories import create_categories
from scripts.migration.origins import create_origins
from scripts.migration.producers import create_producers
from scripts.migration.stores import create_stores
from scripts.migration.users import create_users
from scripts.migration.volumes import create_volume

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def main(
    source: Annotated[str, typer.Argument()] = "dashboard",
    destination: Annotated[str, typer.Argument()] = "temp",
    delete_destination: Annotated[bool, typer.Option("--delete", "-d")] = True,
) -> None:
    src_settings = Settings(mongo_database=source)
    dst_settings = Settings(mongo_database=destination)
    src_context = Context(settings=src_settings)
    dst_context = Context(settings=dst_settings)

    if delete_destination:
        for collection_name in dst_context.database.list_collection_names():
            dst_context.database[collection_name].drop()

    stores = create_stores(src_context=src_context, dst_context=dst_context)

    create_users(
        src_context=src_context,
        dst_context=dst_context,
        stores=stores,
    )

    categories = create_categories(dst_context=dst_context)

    origins = create_origins(dst_context=dst_context)

    articles = create_articles(
        src_context=src_context,
        dst_context=dst_context,
        stores=stores,
        categories=categories,
        origins=origins,
    )

    create_producers(dst_context=dst_context, articles=articles)

    create_volume(
        dst_context=dst_context,
        categories=categories,
        articles=articles,
    )


if __name__ == "__main__":
    app()
