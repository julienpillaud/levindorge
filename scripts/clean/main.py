from typing import Annotated, Any

import typer
from rich.console import Console
from rich.panel import Panel

from app.core.config.settings import Settings
from app.core.core import Context
from app.infrastructure.tactill.utils import INCLUDED_CATEGORIES
from scripts.clean.dashboard import (
    delete_dashboard_articles,
    get_dashboard_articles,
    get_stores,
)
from scripts.clean.entities import Container, Containers
from scripts.clean.pos import build_pos_containers, delete_pos_articles

app = typer.Typer()
console = Console()


@app.command()
def clean(
    category: Annotated[str | None, typer.Argument()],
    all_categories: Annotated[bool, typer.Option("--all")] = False,
    dry_run: Annotated[bool, typer.Option()] = True,
) -> None:
    if all_categories:
        name_or_names: str | list[str] = INCLUDED_CATEGORIES
    else:
        if not category:
            console.print(
                "[bold red]You must specify a category or use --all[/bold red]"
            )
            raise typer.Exit()
        name_or_names = category

    settings = Settings(mongo_database="dashboard")  # ty:ignore[missing-argument]
    context = Context(settings=settings)

    stores = get_stores(context=context)
    containers = build_containers(
        context=context,
        stores=stores,
        name_or_names=name_or_names,
    )
    print_output(containers=containers)
    if not dry_run:
        delete_pos_articles(containers=containers.containers)
        delete_dashboard_articles(context=context, containers=containers.containers)


def build_containers(
    context: Context,
    stores: list[dict[str, Any]],
    name_or_names: str | list[str],
) -> Containers:
    pos_containers = build_pos_containers(
        stores=stores,
        name_or_names=name_or_names,
    )
    dashboard_articles = get_dashboard_articles(
        context=context,
        name_or_names=name_or_names,
    )

    all_references = set(pos_containers.keys()) | set(dashboard_articles.keys())
    containers = [
        Container(
            reference=reference,
            in_dashboard=dashboard_articles.get(reference, False),
            pos=pos_containers.get(reference, []),
        )
        for reference in all_references
    ]
    return Containers(containers=containers)


def print_output(containers: Containers) -> None:
    width = 40
    lines = [
        f"{'Total avant:': <{width}}{containers.total}",
        f"{'Total après :': <{width}}{containers.in_pos_with_stock}",
        f"{'Manquant dashboard après :': <{width}}{containers.only_in_pos_with_stock}",
    ]
    console.print(
        Panel.fit(
            "\n".join(lines),
            title="Suppression Produits",
            border_style="blue",
        )
    )


def format_value(value: int) -> str:
    if value < 0:
        return f"[bold red]{value}[/bold red]"
    return f"[bold green]{value}[/bold green]"
