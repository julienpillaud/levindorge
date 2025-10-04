from typing import TextIO

from PIL import ImageFont

from app.core.config import Settings
from app.domain.articles.entities import Article
from app.domain.commons.entities import PricingGroup
from app.domain.context import ContextProtocol
from app.domain.items.entities import Item, ItemType
from app.domain.price_labels.entities import PriceLabelWrapper
from app.domain.price_labels.utils.common import (
    chunk_price_labels,
    define_beer_name,
    define_name,
    get_file_path,
    normalize_attribute,
)
from app.domain.shops.entities import Shop

MAX_LARGE_LABELS_PER_FILE = 9


def create_large_price_labels(
    context: ContextProtocol,
    settings: Settings,
    current_shop: Shop,
    price_labels: list[PriceLabelWrapper],
) -> None:
    regions_mapping = {
        region.name: region
        for region in context.repository.get_items(ItemType.COUNTRIES)
    }

    for file_index, labels in enumerate(
        chunk_price_labels(
            price_labels=price_labels,
            chunk_size=MAX_LARGE_LABELS_PER_FILE,
        )
    ):
        file_path = get_file_path(
            prefix="large",
            index=file_index,
            shop=current_shop,
            path=settings.app_path.price_labels,
        )

        with open(file_path, "w", encoding="utf-8") as file:
            file.write('{% extends "/price_labels/base_large.html" %}\n')
            file.write("{% block content %}\n")

            write_large_labels_file(
                settings=settings,
                file=file,
                price_labels=labels,
                shop=current_shop,
                regions_mapping=regions_mapping,
            )

            file.write("{% endblock %}\n")


def write_large_labels_file(
    settings: Settings,
    file: TextIO,
    price_labels: list[PriceLabelWrapper],
    shop: Shop,
    regions_mapping: dict[str, Item],
) -> None:
    for index, price_label in enumerate(price_labels):
        write_large_price_labels(
            settings=settings,
            file=file,
            index=index,
            pricing_group=price_label.pricing_group,
            article=price_label.article,
            shop=shop,
            regions_mapping=regions_mapping,
        )


def write_large_price_labels(
    settings: Settings,
    file: TextIO,
    index: int,
    pricing_group: PricingGroup,
    article: Article,
    shop: Shop,
    regions_mapping: dict[str, Item],
) -> None:
    font_file = settings.app_path.fonts / "localbrewerytwo-bold.otf"
    font = ImageFont.truetype(str(font_file), 23)

    color = article.color

    # background
    background = (
        "coffret"
        if pricing_group in {"box", "food", "misc", "others"}
        else normalize_attribute(color)
    )
    file.write(f'<div class="bgClass bgClass{index + 1} {background}">\n')

    # top line
    if pricing_group in {"beer", "keg", "mini_keg"}:
        volume = article.formated_volume(",")
        demonym = regions_mapping[article.region].demonym
        top_line = f"{color} - {volume} - {demonym}"
        file.write(f'<div class="toplinebeerClass brandonClass">{top_line}</div>\n')

    elif pricing_group in {"wine", "sparkling_wine", "bib"}:
        if article.type in {"Vin", "Vin effervescent", "BIB"}:
            top_line = f"{color} - {article.region}"
        else:
            top_line = f"{color} - {article.type}"
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
        name_tag = article.name.name1
        file.write('<div class="nameBoxContainer">\n')
        file.write(f'<div class="nameBoxClass brandonClass">{name_tag}</div>\n')
        file.write("</div>\n")

    # ----------------------------------------------------------
    sell_price = article.shops[shop.username].sell_price
    sell_price_tag = f"{sell_price:.2f}".replace(".", ", ")
    file.write(f'<div class="priceClass">{sell_price_tag} €</div>\n')

    # ----------------------------------------------------------
    if pricing_group == "beer" and article.deposit.unit == 0:
        file.write('<div class="consigneClass"></div>\n')
    elif pricing_group == "beer" and article.deposit.case != 0:
        file.write('<div class="consigneClass">Consigne : 0, 15 €</div>\n')
    elif pricing_group == "mini_keg":
        file.write('<div class="consigneClass">Consigne : 7, 50 €</div>\n')
    elif pricing_group in {"wine", "sparkling_wine", "bib"}:
        volume = article.formated_volume(",")
        file.write(f'<div class="volumeClass">{volume}</div>\n')

    file.write("</div>\n")
