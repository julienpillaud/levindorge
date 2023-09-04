import datetime
import os

import unidecode
from PIL import ImageFont

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAGS_PATH = os.path.join(APP_PATH, "templates", "tags")
FONTS_PATH = os.path.join(APP_PATH, "static", "fonts")

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


class PriceTag(object):
    def __init__(self):
        self.date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    @staticmethod
    def define_color(product, color):
        if product in {"beer", "mini_keg"}:
            return BEER_COLORS[color]
        elif product in {"wine", "sparkling_wine", "bib"}:
            return WINE_COLORS[color]

    @staticmethod
    def define_taste(taste):
        return TASTES[taste]

    @staticmethod
    def convert_volume(category, volume):
        if category in {"bib", "keg", "mini_keg"}:
            volume_tag = volume
            unit = "L"
        elif volume > 100:
            volume_tag = volume / 100
            unit = "L"
        else:
            volume_tag = volume
            unit = "cl"
        volume_tag = str(volume_tag).rstrip("0").rstrip(".").replace(".", ",") + unit
        return volume_tag

    @staticmethod
    def define_beer_name(tag):
        font_file = os.path.join(FONTS_PATH, "localbrewerytwo-bold.otf")
        font = ImageFont.truetype(font_file, 23)
        name1 = tag["name"]["name1"]
        name2 = tag["name"]["name2"]
        if name1 == "":
            length = font.getsize(name2)[0]
            if length > 300:
                i = 1
                test_length = length
                while test_length > length / 2:
                    test_name = name2.rsplit(" ", i)[0]
                    test_length = font.getsize(test_name)[0]
                    i += 1
                name_beer = None
                name_sup_beer = test_name
                name_inf_beer = name2.split(test_name)[1][1:]
            else:
                name_beer = name2
                name_sup_beer = None
                name_inf_beer = None
        else:
            name_beer = None
            name_sup_beer = name1
            name_inf_beer = name2

        return name_beer, name_sup_beer, name_inf_beer

    @staticmethod
    def define_wine_name(tag):
        name1 = tag["name"]["name1"]
        name2 = tag["name"]["name2"]
        if name1 == "":
            name_wine = name2
            name_sup_wine = None
            name_inf_wine = None
        else:
            if name2 == "":
                name_wine = name1
                name_sup_wine = None
                name_inf_wine = None
            else:
                name_wine = None
                name_sup_wine = name1
                name_inf_wine = name2

        return name_wine, name_sup_wine, name_inf_wine

    @staticmethod
    def define_spirit_name(tag):
        name1 = tag["name"]["name1"]
        name2 = tag["name"]["name2"]
        if name1 == "":
            name_spirit = name2
            name_spirit_sup = None
            name_spirit_inf = None
        else:
            if name2 == "":
                name_spirit = name1
                name_spirit_sup = None
                name_spirit_inf = None
            else:
                name_spirit = None
                name_spirit_sup = name1
                name_spirit_inf = name2
        return name_spirit, name_spirit_sup, name_spirit_inf

    @staticmethod
    def chunk_tag_list(tag_list, n):
        expand_tag_list = [i for i, j in tag_list for _ in range(j)]
        for i in range(0, len(expand_tag_list), n):
            yield expand_tag_list[i : i + n]

    def write_beer_tag(self, tag_list, shop_code, demonym_dict):
        for file_index, chunk in enumerate(
            self.chunk_tag_list(tag_list, MAX_BEER_TAGS)
        ):
            date = datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"etiquette_biere-vin_{file_index + 1}_{shop_code}_{date}.html"
            file = os.path.join(TAGS_PATH, file_name)

            with open(file, "w", encoding="utf-8") as f:
                f.write('{% extends "/tags/base_lg.html" %}\n')
                f.write("{% block content %}\n")

                for tag_index, tag in enumerate(chunk):
                    color = tag["color"]

                    # --------------------------------------------------------------------------------------------------
                    if tag["ratio_category"] in {"box", "food", "misc"}:
                        background = "coffret"
                    else:
                        background = self.define_color(tag["ratio_category"], color)
                    f.write(
                        f'<div class="bgClass bgClass{tag_index + 1} {background}">\n'
                    )

                    # --------------------------------------------------------------------------------------------------
                    if tag["ratio_category"] in {"beer", "mini_keg"}:
                        volume = self.convert_volume(tag["ratio_category"], tag["volume"])
                        demonym = demonym_dict[tag["region"]]
                        f.write(
                            f'<div class="toplinebeerClass brandonClass">{color} - {volume} - {demonym}</div>\n'
                        )

                    elif tag["ratio_category"] in {"wine", "sparkling_wine", "bib"}:
                        if tag["type"] in {"Vin", "Vin effervescent", "BIB"}:
                            f.write(
                                f'<div class="toplinewineClass">{color} - {tag["region"]}</div>\n'
                            )
                        else:
                            f.write(
                                f'<div class="toplinewineClass">{color} - {tag["type"]}</div>\n'
                            )

                    # --------------------------------------------------------------------------------------------------
                    if tag["ratio_category"] in {"beer", "mini_keg"}:
                        name_beer, name_sup_beer, name_inf_beer = self.define_beer_name(
                            tag
                        )
                        if name_beer:
                            f.write(f'<div class="nameClass">{name_beer}</div>\n')
                        if name_sup_beer:
                            f.write(
                                f'<div class="nameSupClass">{name_sup_beer}</div>\n'
                            )
                        if name_inf_beer:
                            f.write(
                                f'<div class="nameInfClass">{name_inf_beer}</div>\n'
                            )
                    elif tag["ratio_category"] in {"wine", "sparkling_wine", "bib"}:
                        name_wine, name_sup_wine, name_inf_wine = self.define_wine_name(
                            tag
                        )
                        if name_wine:
                            f.write(f'<div class="nameClass">{name_wine}</div>\n')
                        if name_sup_wine:
                            f.write(
                                f'<div class="nameSupClass">{name_sup_wine}</div>\n'
                            )
                        if name_inf_wine:
                            f.write(
                                f'<div class="nameInfClass">{name_inf_wine}</div>\n'
                            )
                    elif tag["ratio_category"] in ["box", "food", "misc"]:
                        name_tag = tag["name"]["name1"]
                        f.write('<div class="nameBoxContainer">\n')
                        f.write(
                            f'<div class="nameBoxClass brandonClass">{name_tag}</div>\n'
                        )
                        f.write("</div>\n")

                    # --------------------------------------------------------------------------------------------------
                    sell_price = tag["shops"][shop_code]["sell_price"]
                    sell_price_tag = "{:.2f}".format(sell_price).replace(".", ", ")
                    f.write(f'<div class="priceClass">{sell_price_tag} €</div>\n')

                    # --------------------------------------------------------------------------------------------------
                    if tag["ratio_category"] == "beer" and tag["deposit"]["unit"] == 0:
                        f.write('<div class="consigneClass"></div>\n')
                    elif (
                        tag["ratio_category"] == "beer" and tag["deposit"]["case"] != 0
                    ):
                        f.write('<div class="consigneClass">Consigne : 0, 15 €</div>\n')
                    elif tag["ratio_category"] == "mini_keg":
                        f.write('<div class="consigneClass">Consigne : 7, 50 €</div>\n')
                    elif tag["ratio_category"] in {"wine", "sparkling_wine", "bib"}:
                        volume = self.convert_volume(tag["ratio_category"], tag["volume"])
                        f.write(f'<div class="volumeClass">{volume}</div>\n')

                    f.write("</div>\n")

                f.write("{% endblock %}\n")

    def write_spirit_tag(self, tag_list, shop_code):
        for file_index, chunk in enumerate(
            self.chunk_tag_list(tag_list, MAX_SPIRIT_TAGS)
        ):
            date = datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"etiquette_spirit_{file_index + 1}_{shop_code}_{date}.html"
            file = os.path.join(TAGS_PATH, file_name)

            with open(file, "w", encoding="utf-8") as f:
                f.write('{% extends "/tags/base_sm.html" %}\n')
                f.write("{% block content %}\n")

                for tag_index, tag in enumerate(chunk):
                    # --------------------------------------------------------------------------------------------------
                    taste = tag["taste"]
                    (
                        name_spirit,
                        name_spirit_sup,
                        name_spirit_inf,
                    ) = self.define_spirit_name(tag)
                    if taste == "":
                        f.write(f'<div class="bgClass bgClass{tag_index + 1} blanc">\n')
                        if name_spirit:
                            f.write(
                                f'<div class="spiritNameClass grey">{name_spirit}</div>\n'
                            )
                        if name_spirit_sup:
                            f.write(
                                f'<div class="spiritNamesClass grey">{name_spirit_sup}</div>\n'
                            )
                        if name_spirit_inf:
                            f.write(
                                f'<div class="spiritNamesClass grey">{name_spirit_inf}</div>\n'
                            )
                    else:
                        taste_class = self.define_taste(taste)
                        f.write(
                            f'<div class="bgClass bgClass{tag_index + 1} {taste_class}">\n'
                        )
                        if name_spirit:
                            f.write(
                                f'<div class="spiritNameClass">{name_spirit}</div>\n'
                            )
                        if name_spirit_sup:
                            f.write(
                                f'<div class="spiritNamesClass">{name_spirit_sup}</div>\n'
                            )
                        if name_spirit_inf:
                            f.write(
                                f'<div class="spiritNamesClass">{name_spirit_inf}</div>\n'
                            )
                    # --------------------------------------------------------------------------------------------------
                    f.write('<div class="bottomlineClass">\n')
                    # --------------------------------------------------------------------------------------------------
                    volume = self.convert_volume(tag["ratio_category"], tag["volume"])
                    f.write(f'<div class="bottleClass">{volume}</div>')
                    # --------------------------------------------------------------------------------------------------
                    sell_price = tag["shops"][shop_code]["sell_price"]
                    sell_price_tag = "{:.0f}".format(sell_price).replace(".", ", ")
                    f.write(f'<div class="priceClass">{sell_price_tag} €</div>')
                    # --------------------------------------------------------------------------------------------------
                    flag_class = unidecode.unidecode(tag["region"].replace(" ", "_"))
                    f.write(f'<div class="flagClass {flag_class}"></div>\n')
                    # --------------------------------------------------------------------------------------------------
                    f.write("</div>\n")
                    f.write("</div>\n")

                f.write("{% endblock %}\n")
