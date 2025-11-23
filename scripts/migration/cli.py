from typing import Annotated

import typer
from rich.console import Console

from app.core.config import Settings
from app.core.core import Context
from scripts.migration.articles import update_articles
from scripts.migration.categories import update_categories
from scripts.migration.producers import update_producers
from scripts.migration.stores import update_stores
from scripts.migration.users import update_users

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

    update_stores(src_context, dst_context)
    update_users(src_context, dst_context)
    update_categories(dst_context)
    update_articles(src_context, dst_context)
    update_producers(dst_context)


if __name__ == "__main__":
    app()
