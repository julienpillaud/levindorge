import datetime
from io import StringIO
from typing import TextIO

from app.domain.articles.entities import Article
from app.domain.origins.entities import Origin
from app.domain.price_labels.entities import (
    PriceLabelSheet,
    PriceLabelType,
    PriceLabelWrapper,
)
from app.domain.price_labels.utils.common import (
    chunk_price_labels,
    define_name,
    normalize_attribute,
)
from app.domain.stores.entities import Store

MAX_SMALL_LABELS_PER_FILE = 40


def create_small_price_labels(
    store: Store,
    price_label_wrappers: list[PriceLabelWrapper],
    origins_map: dict[str, Origin],
) -> list[PriceLabelSheet]:
    price_labels: list[PriceLabelSheet] = []
    for index, labels in enumerate(
        chunk_price_labels(
            price_labels=price_label_wrappers,
            chunk_size=MAX_SMALL_LABELS_PER_FILE,
        ),
        start=1,
    ):
        buffer = StringIO()
        write_small_labels_file(
            file=buffer,
            price_labels=labels,
            store=store,
            origins_map=origins_map,
        )
        content = buffer.getvalue()
        buffer.close()

        price_labels.append(
            PriceLabelSheet(
                type=PriceLabelType.SMALL,
                store_name=store.name,
                index=index,
                date=datetime.datetime.now(datetime.UTC),
                content=content,
            )
        )

    return price_labels


def write_small_labels_file(
    store: Store,
    file: TextIO,
    price_labels: list[PriceLabelWrapper],
    origins_map: dict[str, Origin],
) -> None:
    for index, price_label in enumerate(price_labels):
        write_small_price_labels(
            file=file,
            index=index,
            article=price_label.article,
            store=store,
            origins_map=origins_map,
        )


def write_small_price_labels(
    file: TextIO,
    store: Store,
    index: int,
    article: Article,
    origins_map: dict[str, Origin],
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
        taste_class = normalize_attribute(article.taste) if article.taste else "blanc"
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
    file.write(f'<div class="bottleClass">{article.volume}</div>\n')
    # ----------------------------------------------------------
    sell_price = article.store_data[store.slug].gross_price
    sell_price_tag = f"{sell_price:.0f}".replace(".", ", ")
    file.write(f'<div class="priceClass">{sell_price_tag} €</div>\n')
    # ----------------------------------------------------------
    origin = origins_map.get(article.origin or "")
    file.write('<div class="flagClass">\n')
    if origin and origin.code:
        file.write(f'<img src="https://flagcdn.com/w160/{origin.code.lower()}.png">')
    file.write("</div>\n")
    # ----------------------------------------------------------
    file.write("</div>\n")
    file.write("</div>\n")
