from collections.abc import Iterator
from datetime import datetime, timezone
from pathlib import Path

import unidecode
from PIL import ImageFont
from PIL.ImageFont import FreeTypeFont

from app.entities.article import TagArticle
from app.entities.item import Item

MAX_BEER_TAGS = 9
MAX_SPIRIT_TAGS = 40

BEER_COLORS = {
    "Blonde": "blonde",
    "Ambrée": "ambree",
    "Brune": "brune",
    "Fruitée": "fruitee",
    "Blanche": "blanche",
}

WINE_COLORS = {"Rouge": "rouge", "Rosé": "rose", "Blanc": "blanc"}

TASTES = {
    "Boisé": "boise",
    "Epicé": "epice",
    "Floral": "floral",
    "Fruité": "fruite",
    "Iodé": "iode",
    "Toasté": "toaste",
    "Tourbé": "tourbe",
    "Végétal": "vegetal",
}


class PriceTag:
    def __init__(self, tags_path: Path, fonts_path: Path) -> None:
        self.tags_path = tags_path
        self.fonts_path = fonts_path
        self.font_file = fonts_path / "localbrewerytwo-bold.otf"
        self.font = ImageFont.truetype(str(self.font_file), 23)

    @staticmethod
    def define_color(product: str, color: str) -> str:
        if product in {"beer", "mini_keg"}:
            return BEER_COLORS[color]
        elif product in {"wine", "sparkling_wine", "bib"}:
            return WINE_COLORS[color]
        else:
            raise ValueError

    @staticmethod
    def define_taste(taste: str) -> str:
        return TASTES[taste]

    @staticmethod
    def convert_volume(category: str, volume: float) -> str:
        if category in {"bib", "keg", "mini_keg"}:
            volume_tag = volume
            unit = "L"
        elif volume > 100:
            volume_tag = volume / 100
            unit = "L"
        else:
            volume_tag = volume
            unit = "cl"
        return str(volume_tag).rstrip("0").rstrip(".").replace(".", ",") + unit

    @staticmethod
    def define_beer_name(
        article: TagArticle, font: FreeTypeFont
    ) -> tuple[str | None, str | None, str | None]:
        name2 = article.name.name2

        if name1 := article.name.name1:
            return None, name1, name2

        length = font.getlength(name2)
        if length <= 300:
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

    @staticmethod
    def define_name(article: TagArticle) -> tuple[str | None, str | None, str | None]:
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

    @staticmethod
    def chunk_tag_list(
        tag_list: list[tuple[TagArticle, int]], n: int
    ) -> Iterator[list[TagArticle]]:
        expand_tag_list = [i for i, j in tag_list for _ in range(j)]
        for i in range(0, len(expand_tag_list), n):
            yield expand_tag_list[i : i + n]

    def write_large_tags(
        self,
        tag_list: list[tuple[TagArticle, int]],
        shop_code: str,
        regions: dict[str, Item],
    ) -> None:
        for file_index, chunk in enumerate(
            self.chunk_tag_list(tag_list, MAX_BEER_TAGS)
        ):
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"etiquette_biere-vin_{file_index + 1}_{shop_code}_{date}.html"
            file = self.tags_path / file_name

            with open(file, "w", encoding="utf-8") as f:
                f.write('{% extends "/tags/base_lg.html" %}\n')
                f.write("{% block content %}\n")

                for tag_index, article in enumerate(chunk):
                    self.write_large_tag(f, tag_index, article, shop_code, regions)

                f.write("{% endblock %}\n")

    def write_large_tag(self, f, tag_index, article, shop_code, regions):  # noqa: C901
        color = article.color

        # ----------------------------------------------------------
        if article.ratio_category in {"box", "food", "misc", "others"}:
            background = "coffret"
        else:
            background = self.define_color(article.ratio_category, color)
        f.write(f'<div class="bgClass bgClass{tag_index + 1} {background}">\n')

        # ----------------------------------------------------------
        if article.ratio_category in {"beer", "mini_keg"}:
            volume = self.convert_volume(article.ratio_category, article.volume)
            demonym = regions[article.region].demonym
            top_line = f"{color} - {volume} - {demonym}"
            f.write(f'<div class="toplinebeerClass brandonClass">{top_line}</div>\n')

        elif article.ratio_category in {"wine", "sparkling_wine", "bib"}:
            if article.type in {"Vin", "Vin effervescent", "BIB"}:
                top_line = f"{color} - {article.region}"
            else:
                top_line = f"{color} - {article.type}"
            f.write(f'<div class="toplinewineClass">{top_line}</div>\n')
        # ----------------------------------------------------------
        if article.ratio_category in {"beer", "mini_keg"}:
            name_beer, name_sup_beer, name_inf_beer = self.define_beer_name(
                article, self.font
            )
            if name_beer:
                f.write(f'<div class="nameClass">{name_beer}</div>\n')
            if name_sup_beer:
                f.write(f'<div class="nameSupClass">{name_sup_beer}</div>\n')
            if name_inf_beer:
                f.write(f'<div class="nameInfClass">{name_inf_beer}</div>\n')
        elif article.ratio_category in {"wine", "sparkling_wine", "bib"}:
            name_wine, name_sup_wine, name_inf_wine = self.define_name(article)
            if name_wine:
                f.write(f'<div class="nameClass">{name_wine}</div>\n')
            if name_sup_wine:
                f.write(f'<div class="nameSupClass">{name_sup_wine}</div>\n')
            if name_inf_wine:
                f.write(f'<div class="nameInfClass">{name_inf_wine}</div>\n')
        elif article.ratio_category in ["box", "food", "misc", "others"]:
            name_tag = article.name.name1
            f.write('<div class="nameBoxContainer">\n')
            f.write(f'<div class="nameBoxClass brandonClass">{name_tag}</div>\n')
            f.write("</div>\n")

        # ----------------------------------------------------------
        sell_price = article.shops[shop_code].sell_price
        sell_price_tag = f"{sell_price:.2f}".replace(".", ", ")
        f.write(f'<div class="priceClass">{sell_price_tag} €</div>\n')

        # ----------------------------------------------------------
        if article.ratio_category == "beer" and article.deposit.unit == 0:
            f.write('<div class="consigneClass"></div>\n')
        elif article.ratio_category == "beer" and article.deposit.case != 0:
            f.write('<div class="consigneClass">Consigne : 0, 15 €</div>\n')
        elif article.ratio_category == "mini_keg":
            f.write('<div class="consigneClass">Consigne : 7, 50 €</div>\n')
        elif article.ratio_category in {"wine", "sparkling_wine", "bib"}:
            volume = self.convert_volume(article.ratio_category, article.volume)
            f.write(f'<div class="volumeClass">{volume}</div>\n')

        f.write("</div>\n")

    def write_small_tags(
        self, tag_list: list[tuple[TagArticle, int]], shop_code: str
    ) -> None:
        for file_index, chunk in enumerate(
            self.chunk_tag_list(tag_list, MAX_SPIRIT_TAGS)
        ):
            date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"etiquette_spirit_{file_index + 1}_{shop_code}_{date}.html"
            file = self.tags_path / file_name

            with open(file, "w", encoding="utf-8") as f:
                f.write('{% extends "/tags/base_sm.html" %}\n')
                f.write("{% block content %}\n")

                for tag_index, article in enumerate(chunk):
                    self.write_small_tag(f, tag_index, article, shop_code)

                f.write("{% endblock %}\n")

    def write_small_tag(self, f, tag_index, article, shop_code):
        taste = article.taste
        (
            name_spirit,
            name_spirit_sup,
            name_spirit_inf,
        ) = self.define_name(article)
        if taste == "":
            f.write(f'<div class="bgClass bgClass{tag_index + 1} blanc">\n')
            if name_spirit:
                f.write(f'<div class="spiritNameClass grey">{name_spirit}</div>\n')
            if name_spirit_sup:
                f.write(f'<div class="spiritNamesClass grey">{name_spirit_sup}</div>\n')
            if name_spirit_inf:
                f.write(f'<div class="spiritNamesClass grey">{name_spirit_inf}</div>\n')
        else:
            taste_class = self.define_taste(taste)
            f.write(f'<div class="bgClass bgClass{tag_index + 1} {taste_class}">\n')
            if name_spirit:
                f.write(f'<div class="spiritNameClass">{name_spirit}</div>\n')
            if name_spirit_sup:
                f.write(f'<div class="spiritNamesClass">{name_spirit_sup}</div>\n')
            if name_spirit_inf:
                f.write(f'<div class="spiritNamesClass">{name_spirit_inf}</div>\n')
        # ----------------------------------------------------------
        f.write('<div class="bottomlineClass">\n')
        # ----------------------------------------------------------
        volume = self.convert_volume(article.ratio_category, article.volume)
        f.write(f'<div class="bottleClass">{volume}</div>')
        # ----------------------------------------------------------
        sell_price = article.shops[shop_code].sell_price
        sell_price_tag = f"{sell_price:.0f}".replace(".", ", ")
        f.write(f'<div class="priceClass">{sell_price_tag} €</div>')
        # ----------------------------------------------------------
        flag_class = unidecode.unidecode(article.region.replace(" ", "_"))
        f.write(f'<div class="flagClass {flag_class}"></div>\n')
        # ----------------------------------------------------------
        f.write("</div>\n")
        f.write("</div>\n")
