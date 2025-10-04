from typing import Annotated, Any

import typer
from pymongo import MongoClient
from rich.console import Console

from app.core.config import Settings

app = typer.Typer()
console = Console()


def get_settings() -> Settings:
    return Settings(_env_file=".env")


def get_client() -> MongoClient[dict[str, Any]]:
    settings = get_settings()
    return MongoClient(settings.mongo_uri)


@app.command()
def copy(
    source: Annotated[str, typer.Argument()],
    target: Annotated[str, typer.Argument()],
    input_collections: Annotated[
        list[str] | None, typer.Option("--collections", "-c")
    ] = None,
) -> None:
    if input_collections is None:
        input_collections = []

    client = get_client()
    assert_source_target_are_valid(client=client, source=source, target=target)
    collections = get_collections_to_copy(
        client=client,
        source=source,
        collections=input_collections,
    )

    console.print(f"[magenta]Copying '{source}' to '{target}'[/magenta]")
    for collection_name in collections:
        source_collection = client[source][collection_name]
        documents = list(source_collection.find())
        if not documents:
            continue
        console.print(f"Copying '{collection_name}' ({len(documents)} documents)")

        target_collection = client[target][collection_name]
        result = target_collection.insert_many(documents)
        console.print(f"Inserted {len(result.inserted_ids)} documents")


def assert_source_target_are_valid(
    client: MongoClient[dict[str, Any]],
    source: str,
    target: str,
) -> None:
    existing_dbs = client.list_database_names()

    if target in existing_dbs:
        console.print(f"[red]Target '{target}' already exists[/red]")
        raise typer.Exit()

    if source not in existing_dbs:
        console.print(f"[red]Source '{source}' does not exist[/red]")
        raise typer.Exit()


def get_collections_to_copy(
    client: MongoClient[dict[str, Any]],
    source: str,
    collections: list[str],
) -> list[str]:
    existing_collections = client[source].list_collection_names()
    if not collections:
        return existing_collections

    if any(collection not in existing_collections for collection in collections):
        console.print("[red]Some collections do not exist[/red]")
        raise typer.Exit()

    return collections


@app.command()
def drop(database: Annotated[str, typer.Argument()]) -> None:
    if database == "dashboard":
        raise ValueError("Cannot drop the dashboard database")

    client_instance = get_client()
    client_instance.drop_database(database)
    console.print(f"[green]Database '{database}' dropped successfully![/green]")


if __name__ == "__main__":
    app()
