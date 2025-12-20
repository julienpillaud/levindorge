import datetime
from io import StringIO
from typing import TextIO

from PIL import ImageFont

from app.core.config.settings import Settings
from app.domain.articles.entities import Article
from app.domain.commons.entities import PricingGroup
from app.domain.price_labels.entities import (
    PriceLabelSheet,
    PriceLabelType,
    PriceLabelWrapper,
)
from app.domain.price_labels.utils.common import (
    chunk_price_labels,
    define_beer_name,
    define_name,
    normalize_attribute,
)
from app.domain.stores.entities import Store

MAX_LARGE_LABELS_PER_FILE = 9


def create_large_price_labels(
    settings: Settings,
    store: Store,
    price_label_wrappers: list[PriceLabelWrapper],
) -> list[PriceLabelSheet]:
    price_labels: list[PriceLabelSheet] = []
    for index, labels in enumerate(
        chunk_price_labels(
            price_labels=price_label_wrappers,
            chunk_size=MAX_LARGE_LABELS_PER_FILE,
        ),
        start=1,
    ):
        buffer = StringIO()
        write_large_labels_file(
            settings=settings,
            file=buffer,
            price_labels=labels,
            store=store,
        )
        content = buffer.getvalue()
        buffer.close()

        price_labels.append(
            PriceLabelSheet(
                type=PriceLabelType.LARGE,
                store_name=store.name,
                index=index,
                date=datetime.datetime.now(datetime.UTC),
                content=content,
            )
        )

    return price_labels


def write_large_labels_file(
    settings: Settings,
    store: Store,
    file: TextIO,
    price_labels: list[PriceLabelWrapper],
) -> None:
    for index, price_label in enumerate(price_labels):
        write_large_price_labels(
            settings=settings,
            file=file,
            index=index,
            pricing_group=price_label.pricing_group,
            article=price_label.article,
            store=store,
        )


def write_large_price_labels(
    settings: Settings,
    store: Store,
    file: TextIO,
    index: int,
    pricing_group: PricingGroup,
    article: Article,
) -> None:
    font_file = settings.app_path.fonts / "localbrewerytwo-bold.otf"
    font = ImageFont.truetype(str(font_file), 23)

    color = article.color or ""

    # background
    background = (
        "coffret"
        if pricing_group in {PricingGroup.BOX, PricingGroup.OTHER}
        else normalize_attribute(color)
    )
    file.write(f'<div class="bgClass bgClass{index + 1} {background}">\n')

    # top line
    if pricing_group in {
        PricingGroup.BEER,
        PricingGroup.KEG,
        PricingGroup.MINI_KEG,
    }:
        top_line = f"{color} - {article.volume} - {article.origin}"
        file.write(f'<div class="toplinebeerClass brandonClass">{top_line}</div>\n')

    elif pricing_group in {PricingGroup.WINE, PricingGroup.BIB}:
        if article.category in {"Vin", "Vin effervescent", "BIB"}:
            top_line = f"{color} - {article.origin}"
        else:
            top_line = f"{color} - {article.category}"
        file.write(f'<div class="toplinewineClass">{top_line}</div>\n')

    # ----------------------------------------------------------
    if pricing_group in {
        PricingGroup.BEER,
        PricingGroup.KEG,
        PricingGroup.MINI_KEG,
    }:
        name_beer, name_sup_beer, name_inf_beer = define_beer_name(article, font)
        if name_beer:
            file.write(f'<div class="nameClass">{name_beer}</div>\n')
        if name_sup_beer:
            file.write(f'<div class="nameSupClass">{name_sup_beer}</div>\n')
        if name_inf_beer:
            file.write(f'<div class="nameInfClass">{name_inf_beer}</div>\n')

    elif pricing_group in {PricingGroup.WINE, PricingGroup.BIB}:
        name_wine, name_sup_wine, name_inf_wine = define_name(article)
        if name_wine:
            file.write(f'<div class="nameClass">{name_wine}</div>\n')
        if name_sup_wine:
            file.write(f'<div class="nameSupClass">{name_sup_wine}</div>\n')
        if name_inf_wine:
            file.write(f'<div class="nameInfClass">{name_inf_wine}</div>\n')

    elif pricing_group in {PricingGroup.BOX, PricingGroup.OTHER}:
        name_tag = article.product
        file.write('<div class="nameBoxContainer">\n')
        file.write(f'<div class="nameBoxClass brandonClass">{name_tag}</div>\n')
        file.write("</div>\n")

    # ----------------------------------------------------------
    sell_price = article.store_data[store.slug].gross_price
    sell_price_tag = f"{sell_price:.2f}".replace(".", ", ")
    file.write(f'<div class="priceClass">{sell_price_tag} €</div>\n')

    # ----------------------------------------------------------
    if (
        pricing_group == PricingGroup.BEER
        and article.deposit
        and article.deposit.unit == 0
    ):
        file.write('<div class="consigneClass"></div>\n')
    elif (
        pricing_group == PricingGroup.BEER
        and article.deposit
        and article.deposit.case != 0
    ):
        file.write('<div class="consigneClass">Consigne : 0, 15 €</div>\n')
    elif pricing_group == PricingGroup.MINI_KEG:
        file.write('<div class="consigneClass">Consigne : 7, 50 €</div>\n')
    elif pricing_group in {PricingGroup.WINE, PricingGroup.BIB}:
        file.write(f'<div class="volumeClass">{article.volume}</div>\n')

    file.write("</div>\n")
