import datetime
import itertools
from collections.abc import Iterator
from pathlib import Path

from PIL.ImageFont import FreeTypeFont

from app.domain.articles.entities import Article
from app.domain.commons.entities import PricingGroup
from app.domain.context import ContextProtocol
from app.domain.price_labels.entities import PriceLabelCreate, PriceLabelWrapper
from app.domain.shops.entities import Shop

LARGE_LABELS_CATEGORY = {
    PricingGroup.BEER,
    PricingGroup.KEG,
    PricingGroup.MINI_KEG,
    PricingGroup.WINE,
    PricingGroup.BIB,
    PricingGroup.BOX,
    PricingGroup.OTHERS,
}
SMALL_LABEL_CATEGORY = {
    PricingGroup.SPIRIT,
    PricingGroup.ARRANGED,
}
ATTRIBUTES_MAPPING = {
    # beer
    "Blonde": "blonde",
    "Ambrée": "ambree",
    "Brune": "brune",
    "Fruitée": "fruitee",
    "Blanche": "blanche",
    # wine
    "Rouge": "rouge",
    "Rosé": "rose",
    "Blanc": "blanc",
    # spirit
    "Boisé": "boise",
    "Epicé": "epice",
    "Floral": "floral",
    "Fruité": "fruite",
    "Iodé": "iode",
    "Toasté": "toaste",
    "Tourbé": "tourbe",
    "Végétal": "vegetal",
}
LITER_TO_CENTILITER = 100
MAX_NAME_LENGTH = 300


def split_by_size(
    context: ContextProtocol,
    price_labels: list[PriceLabelCreate],
) -> tuple[list[PriceLabelWrapper], list[PriceLabelWrapper]]:
    article_types_mapping = {
        article_type.name: article_type
        for article_type in context.repository.get_article_types()
    }

    large_labels = []
    small_labels = []
    for item in price_labels:
        article = context.repository.get_article(article_id=item.article_id)
        pricing_group = article_types_mapping[article.type].pricing_group

        wrapper = PriceLabelWrapper(
            article=article,
            pricing_group=pricing_group,
            label_count=item.label_count,
        )
        if pricing_group in LARGE_LABELS_CATEGORY:
            large_labels.append(wrapper)
        if pricing_group in SMALL_LABEL_CATEGORY:
            small_labels.append(wrapper)

    return large_labels, small_labels


def chunk_price_labels(
    price_labels: list[PriceLabelWrapper],
    *,
    chunk_size: int,
) -> Iterator[list[PriceLabelWrapper]]:
    iterator = (
        label
        for item in price_labels
        for label in itertools.repeat(item, item.label_count)
    )
    while True:
        chunk = list(itertools.islice(iterator, chunk_size))
        if not chunk:
            break
        yield chunk


def get_file_path(prefix: str, index: int, shop: Shop, path: Path) -> Path:
    date = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{prefix}_{index + 1}_{shop.username}_{date}.html"
    return path / file_name


def normalize_attribute(attr: str) -> str:
    return ATTRIBUTES_MAPPING[attr]


def convert_volume(article: Article) -> str:
    if not article.volume:
        return ""

    value, unit = article.volume.value, article.volume.unit
    if unit == "cL" and value > LITER_TO_CENTILITER:
        value = value / 100
        unit = "L"

    formatted_value = str(value).rstrip("0").rstrip(".").replace(".", ",")
    return f"{formatted_value}{unit}"


def define_beer_name(
    article: Article,
    font: FreeTypeFont,
) -> tuple[str | None, str | None, str | None]:
    name1 = article.name.name1
    name2 = article.name.name2

    if name1:
        return None, name1, name2

    length = font.getlength(name2)

    if length <= MAX_NAME_LENGTH:
        return name2, None, None

    i = 1
    test_length = length
    test_name = name2
    while test_length > length / 2:
        test_name = name2.rsplit(" ", i)[0]
        test_length = font.getlength(test_name)
        i += 1
    name_beer = None
    name_sup_beer = test_name
    name_inf_beer = name2.split(test_name)[1][1:]

    return name_beer, name_sup_beer, name_inf_beer


def define_name(article: Article) -> tuple[str | None, str | None, str | None]:
    name1 = article.name.name1
    name2 = article.name.name2

    if name1 == "":
        name = name2
        name_sup = None
        name_inf = None
    elif name2 == "":
        name = name1
        name_sup = None
        name_inf = None
    else:
        name = None
        name_sup = name1
        name_inf = name2

    return name, name_sup, name_inf
