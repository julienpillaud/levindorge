from typing import TextIO

from app.core.config.settings import Settings
from app.domain.articles.entities import Article
from app.domain.price_labels.entities import PriceLabelWrapper
from app.domain.price_labels.utils.common import (
    chunk_price_labels,
    define_name,
    get_file_path,
    normalize_attribute,
)
from app.domain.types import StoreSlug

MAX_SMALL_LABELS_PER_FILE = 40


def create_small_price_labels(
    settings: Settings,
    store_slug: StoreSlug,
    price_labels: list[PriceLabelWrapper],
) -> None:
    for file_index, labels in enumerate(
        chunk_price_labels(
            price_labels=price_labels,
            chunk_size=MAX_SMALL_LABELS_PER_FILE,
        )
    ):
        file_path = get_file_path(
            prefix="small",
            index=file_index,
            store_slug=store_slug,
            path=settings.app_path.price_labels,
        )

        with open(file_path, "w", encoding="utf-8") as file:
            file.write('{% extends "/price_labels/base_small.html" %}\n')
            file.write("{% block content %}\n")

            write_small_labels_file(
                file=file,
                price_labels=labels,
                store_slug=store_slug,
            )

            file.write("{% endblock %}\n")


def write_small_labels_file(
    file: TextIO,
    price_labels: list[PriceLabelWrapper],
    store_slug: StoreSlug,
) -> None:
    for index, price_label in enumerate(price_labels):
        write_small_price_labels(
            file=file,
            index=index,
            article=price_label.article,
            store_slug=store_slug,
        )


def write_small_price_labels(
    file: TextIO,
    index: int,
    article: Article,
    store_slug: StoreSlug,
) -> None:
    name_spirit, name_spirit_sup, name_spirit_inf = define_name(article=article)

    if article.taste == "":
        file.write(f'<div class="bgClass bgClass{index + 1} blanc">\n')
        if name_spirit:
            file.write(f'<div class="spiritNameClass grey">{name_spirit}</div>\n')
        if name_spirit_sup:
            file.write(f'<div class="spiritNamesClass grey">{name_spirit_sup}</div>\n')
        if name_spirit_inf:
            file.write(f'<div class="spiritNamesClass grey">{name_spirit_inf}</div>\n')
    else:
        taste_class = normalize_attribute(article.taste or "")
        file.write(f'<div class="bgClass bgClass{index + 1} {taste_class}">\n')
        if name_spirit:
            file.write(f'<div class="spiritNameClass">{name_spirit}</div>\n')
        if name_spirit_sup:
            file.write(f'<div class="spiritNamesClass">{name_spirit_sup}</div>\n')
        if name_spirit_inf:
            file.write(f'<div class="spiritNamesClass">{name_spirit_inf}</div>\n')

    # ----------------------------------------------------------
    file.write('<div class="bottomlineClass">\n')
    # ----------------------------------------------------------
    file.write(f'<div class="bottleClass">{article.volume}</div>')
    # ----------------------------------------------------------
    sell_price = article.store_data[store_slug].gross_price
    sell_price_tag = f"{sell_price:.0f}".replace(".", ", ")
    file.write(f'<div class="priceClass">{sell_price_tag} €</div>')
    # ----------------------------------------------------------
    # TODO: get flag from external API
    flag_class = ""
    # flag_class = unidecode.unidecode(article.origin.replace(" ", "_"))
    file.write(f'<div class="flagClass {flag_class}"></div>\n')
    # ----------------------------------------------------------
    file.write("</div>\n")
    file.write("</div>\n")
