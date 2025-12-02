from typing import Any, TextIO

from PIL import ImageFont

from app.core.config import Settings
from app.domain.articles.entities import Article
from app.domain.commons.entities import PricingGroup
from app.domain.context import ContextProtocol
from app.domain.price_labels.entities import PriceLabelWrapper
from app.domain.price_labels.utils.common import (
    chunk_price_labels,
    define_beer_name,
    define_name,
    get_file_path,
    normalize_attribute,
)
from app.domain.stores.entities import Store

MAX_LARGE_LABELS_PER_FILE = 9


def create_large_price_labels(
    context: ContextProtocol,
    settings: Settings,
    current_store: Store,
    price_labels: list[PriceLabelWrapper],
) -> None:
    # TODO: get from new 'origins' repository
    regions_mapping: dict[str, Any] = {}
    # regions_mapping = {
    #     region.name: region
    #     for region in context.repository.get_items(ItemType.COUNTRIES)
    # }

    for file_index, labels in enumerate(
        chunk_price_labels(
            price_labels=price_labels,
            chunk_size=MAX_LARGE_LABELS_PER_FILE,
        )
    ):
        file_path = get_file_path(
            prefix="large",
            index=file_index,
            store=current_store,
            path=settings.app_path.price_labels,
        )

        with open(file_path, "w", encoding="utf-8") as file:
            file.write('{% extends "/price_labels/base_large.html" %}\n')
            file.write("{% block content %}\n")

            write_large_labels_file(
                settings=settings,
                file=file,
                price_labels=labels,
                store=current_store,
                regions_mapping=regions_mapping,
            )

            file.write("{% endblock %}\n")


def write_large_labels_file(
    settings: Settings,
    file: TextIO,
    price_labels: list[PriceLabelWrapper],
    store: Store,
    regions_mapping: dict[str, Any],
) -> None:
    for index, price_label in enumerate(price_labels):
        write_large_price_labels(
            settings=settings,
            file=file,
            index=index,
            pricing_group=price_label.pricing_group,
            article=price_label.article,
            store=store,
            regions_mapping=regions_mapping,
        )


def write_large_price_labels(
    settings: Settings,
    file: TextIO,
    index: int,
    pricing_group: PricingGroup,
    article: Article,
    store: Store,
    regions_mapping: dict[str, Any],
) -> None:
    font_file = settings.app_path.fonts / "localbrewerytwo-bold.otf"
    font = ImageFont.truetype(str(font_file), 23)

    color = article.color or ""

    # background
    background = (
        "coffret"
        if pricing_group in {"box", "food", "misc", "others"}
        else normalize_attribute(color)
    )
    file.write(f'<div class="bgClass bgClass{index + 1} {background}">\n')

    # top line
    if pricing_group in {"beer", "keg", "mini_keg"}:
        demonym = ""  # TODO: replace by country name
        top_line = f"{color} - {article.volume} - {demonym}"
        file.write(f'<div class="toplinebeerClass brandonClass">{top_line}</div>\n')

    elif pricing_group in {"wine", "sparkling_wine", "bib"}:
        if article.category in {"Vin", "Vin effervescent", "BIB"}:
            top_line = f"{color} - {article.origin}"
        else:
            top_line = f"{color} - {article.category}"
        file.write(f'<div class="toplinewineClass">{top_line}</div>\n')

    # ----------------------------------------------------------
    if pricing_group in {"beer", "keg", "mini_keg"}:
        name_beer, name_sup_beer, name_inf_beer = define_beer_name(article, font)
        if name_beer:
            file.write(f'<div class="nameClass">{name_beer}</div>\n')
        if name_sup_beer:
            file.write(f'<div class="nameSupClass">{name_sup_beer}</div>\n')
        if name_inf_beer:
            file.write(f'<div class="nameInfClass">{name_inf_beer}</div>\n')

    elif pricing_group in {"wine", "sparkling_wine", "bib"}:
        name_wine, name_sup_wine, name_inf_wine = define_name(article)
        if name_wine:
            file.write(f'<div class="nameClass">{name_wine}</div>\n')
        if name_sup_wine:
            file.write(f'<div class="nameSupClass">{name_sup_wine}</div>\n')
        if name_inf_wine:
            file.write(f'<div class="nameInfClass">{name_inf_wine}</div>\n')

    elif pricing_group in {"box", "food", "misc", "others"}:
        name_tag = article.product
        file.write('<div class="nameBoxContainer">\n')
        file.write(f'<div class="nameBoxClass brandonClass">{name_tag}</div>\n')
        file.write("</div>\n")

    # ----------------------------------------------------------
    sell_price = article.store_data[store.slug].gross_price
    sell_price_tag = f"{sell_price:.2f}".replace(".", ", ")
    file.write(f'<div class="priceClass">{sell_price_tag} €</div>\n')

    # ----------------------------------------------------------
    if pricing_group == "beer" and article.deposit and article.deposit.unit == 0:
        file.write('<div class="consigneClass"></div>\n')
    elif pricing_group == "beer" and article.deposit and article.deposit.case != 0:
        file.write('<div class="consigneClass">Consigne : 0, 15 €</div>\n')
    elif pricing_group == "mini_keg":
        file.write('<div class="consigneClass">Consigne : 7, 50 €</div>\n')
    elif pricing_group in {"wine", "sparkling_wine", "bib"}:
        file.write(f'<div class="volumeClass">{article.volume}</div>\n')

    file.write("</div>\n")
