from typing import Annotated, Any

import typer
from app.domain.shops.entities import Shop
from rich.console import Console

from app.core.config import Settings
from app.core.core import Context
from app.domain.articles.utils import compute_article_margins, compute_recommended_price
from app.domain.commons.entities import ArticleType

app = typer.Typer()
console = Console()


def taxfree_price(article: dict[str, Any]) -> float:
    taxfree_price_sum = sum(
        [
            article["buy_price"],
            article["excise_duty"],
            article["social_security_levy"],
        ]
    )
    return round(taxfree_price_sum, 4)


def update_article(
    shops: list[Shop],
    article_types_mapping: dict[str, ArticleType],
    article: dict[str, Any],
) -> None:
    article_type = article_types_mapping[article["type"]]
    pricing_group = article_type.pricing_group
    for shop in shops:
        recommended_price = compute_recommended_price(
            total_cost=taxfree_price(article),
            vat_rate=article["tax"],
            shop_margins=shop.margins[pricing_group],
            pricing_group=pricing_group,
        )
        article["shops"][shop.username]["recommended_price"] = recommended_price

        margins = compute_article_margins(
            total_cost=taxfree_price(article),
            tax_rate=article["tax"],
            gross_price=article["shops"][shop.username]["sell_price"],
        )
        article["shops"][shop.username]["margins"] = {}
        article["shops"][shop.username]["margins"]["margin"] = margins.margin_amount
        article["shops"][shop.username]["margins"]["markup"] = margins.margin_rate


def update_articles(context: Context, articles: list[dict[str, Any]]) -> None:
    shops = context.repository.get_shops()
    article_types_mapping = {
        article_type.name: article_type
        for article_type in context.repository.get_article_types()
    }
    for article in articles:
        update_article(shops, article_types_mapping, article)


@app.command()
def migrate(
    destination: Annotated[str, typer.Argument()],
) -> None:
    console.print(
        f"[bold magenta]Migration from 'dashboard' to '{destination}'[/bold magenta]"
    )
    src_settings = Settings(mongo_database="dashboard")
    context = Context(settings=src_settings)

    dst_settings = Settings(mongo_database=destination)
    dst_context = Context(settings=dst_settings)

    for collection_name in context.database.list_collection_names():
        documents = list(context.database[collection_name].find())
        if not documents:
            continue
        console.print(f"    Copying '{collection_name}' ({len(documents)} documents)")
        if collection_name == "articles":
            update_articles(context, documents)

        target_collection = dst_context.database[collection_name]
        result = target_collection.insert_many(documents)
        console.print(f"    Inserted {len(result.inserted_ids)} documents")


@app.command()
def drop(database: Annotated[str, typer.Argument()]) -> None:
    if database == "dashboard":
        console.print("[bold red]Cannot drop 'dashboard' database![/bold red]")
        raise typer.Exit()

    src_settings = Settings()
    context = Context(settings=src_settings)
    context.client.drop_database(database)
    console.print(f"[green]Database '{database}' dropped successfully![/green]")


if __name__ == "__main__":
    app()
