import datetime
import math
from collections import OrderedDict

from application.blueprints.auth import Role


def calculate_recommended_price(taxfree_price, tax, ratio_category, margins):
    """Calculate recommended price"""
    ratio, operator, decimal_round = margins.values()

    if ratio_category == "spirit" and taxfree_price >= 100:
        ratio += 10

    if operator == "+":
        price = (taxfree_price + ratio) * (1 + tax / 100)
    else:
        price = (taxfree_price * ratio) * (1 + tax / 100)

    if decimal_round < 0.1:
        return math.ceil(price * (1 / decimal_round)) / (1 / decimal_round)

    return round(price * (1 / decimal_round)) / (1 / decimal_round)


def calculate_profit(taxfree_price, tax, sell_price):
    """Calculate profit"""
    return (sell_price / (1 + tax / 100)) - taxfree_price


def calculate_margin(tax, sell_price, article_profit):
    """Calculate margin"""
    try:
        article_margin = article_profit / (sell_price / (1 + tax / 100)) * 100
    except ZeroDivisionError:
        article_margin = 0

    return article_margin


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def format_float(f):
    return str(f).rstrip("0").rstrip(".")


def format_date(date):
    return date.strftime("%d / %m / %Y")


def update_price(
    old_taxfree_price, new_taxfree_price, tax, sell_price, ratio_category, margins
):
    decimal_round = margins["decimal_round"]

    if ratio_category == "others":
        new_sell_price = sell_price * new_taxfree_price / old_taxfree_price
    else:
        old_rp = calculate_recommended_price(
            old_taxfree_price, tax, ratio_category, margins
        )
        new_rp = calculate_recommended_price(
            new_taxfree_price, tax, ratio_category, margins
        )
        new_sell_price = sell_price - old_rp + new_rp

    if decimal_round < 0.1:
        return math.ceil(new_sell_price * (1 / decimal_round)) / (1 / decimal_round)
    else:
        return round(new_sell_price * (1 / decimal_round)) / (1 / decimal_round)


# ======================================================================================================================
#  TAG
tag_beer_category = [
    "beer",
    "cider",
    "mini_keg",
    "wine",
    "fortified_wine",
    "sparkling_wine",
    "bib",
    "box",
    "food",
    "misc",
]
tag_spirit_category = ["spirit", "arranged"]


def format_tag_list(tag_list):
    tag_beer_list = []
    tag_spirit_list = []
    for article, nb_tag in tag_list:
        # article['nb_tag'] = nb_tag
        if article["ratio_category"] in tag_beer_category:
            tag_beer_list.append((article, nb_tag))
        elif article["ratio_category"] in tag_spirit_category:
            tag_spirit_list.append((article, nb_tag))

    return tag_beer_list, tag_spirit_list


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# FORMAT_ARTICLES_TO_LIST
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def format_articles_to_list(articles, ratio_category, shops_margins, shop):
    for article in articles:
        # ------------------------------------------------------------------------------
        # 17 VOLUME
        article["volume"] = format_float(article["volume"])
        # ------------------------------------------------------------------------------
        # 18 ALCOHOL_BY_VOLUME
        article["alcohol_by_volume"] = format_float(article["alcohol_by_volume"])
        # ------------------------------------------------------------------------------
        # PRICE
        article["taxfree_price"] = (
            article["buy_price"]
            + article["excise_duty"]
            + article["social_security_levy"]
        )

        margins = shops_margins[shop]["margins"][ratio_category]
        article["recommended_price"] = calculate_recommended_price(
            article["taxfree_price"], article["tax"], ratio_category, margins
        )
        article["recommended_price"] = format_float(article["recommended_price"])

        sell_price = article["shops"][shop]["sell_price"]
        article["margin"] = {}
        article_profit = calculate_profit(
            article["taxfree_price"], article["tax"], sell_price
        )
        article["margin"]["margin"] = round(article_profit, 2)
        article_margin = calculate_margin(article["tax"], sell_price, article_profit)
        article["margin"]["markup"] = round(article_margin)

        article["shops"][shop]["sell_price"] = format_float(
            article["shops"][shop]["sell_price"]
        )
        article["taxfree_price"] = round(article["taxfree_price"], 4)
        # ------------------------------------------------------------------------------
        # STOCK
        for x in article["shops"]:
            if article["shops"][x]["stock_quantity"] == 0:
                article["shops"][x]["stock_quantity"] = ""
        # ------------------------------------------------------------------------------
        # PACKAGING
        if article["packaging"] == 0:
            article["packaging"] = ""
        # ------------------------------------------------------------------------------
        # DEPOSIT
        if article["deposit"]["unit"] == 0:
            article["deposit"]["unit"] = ""
        else:
            article["deposit"]["unit"] = format_float(article["deposit"]["unit"])

        if article["deposit"]["case"] == 0:
            article["deposit"]["case"] = ""
        else:
            article["deposit"]["case"] = format_float(article["deposit"]["case"])

    return articles


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# FORMAT_ARTICLES_TO_UPDATE
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def format_articles_to_update(article, ratio_category):
    # ------------------------------------------------------------------------------
    # DATE
    article["created_at"] = format_date(article["created_at"])
    # ------------------------------------------------------------------------------
    # PRICE
    article["buy_price"] = format_float(article["buy_price"])
    article["excise_duty"] = format_float(article["excise_duty"])
    article["social_security_levy"] = format_float(article["social_security_levy"])
    article["tax"] = format_float(article["tax"])
    # ------------------------------------------------------------------------------
    # SHOPS
    for shop in article["shops"]:
        article["shops"][shop]["sell_price"] = format_float(
            article["shops"][shop]["sell_price"]
        )
        article["shops"][shop]["bar_price"] = format_float(
            article["shops"][shop]["bar_price"]
        )
    # ------------------------------------------------------------------------------
    # VOLUME
    article["volume"] = format_float(article["volume"])
    # ------------------------------------------------------------------------------
    # ALCOHOL_BY_VOLUME
    article["alcohol_by_volume"] = format_float(article["alcohol_by_volume"])
    # ------------------------------------------------------------------------------
    # NAME
    if article["name"]["name1"] == "":
        article["name"]["name1"] = "-"
    # TASTE
    if article["taste"] == "":
        article["taste"] = "-"
    # ------------------------------------------------------------------------------
    # FOOD_PAIRING
    article["food_pairing"] = article["food_pairing"] + ["-"] * (
        6 - len(article["food_pairing"])
    )
    # ------------------------------------------------------------------------------
    # BIO
    if article["biodynamic"] == "":
        article["biodynamic"] = "-"

    return article


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# FORMAT_ARTICLES_TO_VALIDATE
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def format_articles_to_validate(articles, types_dict):
    for article in articles:
        list_category = types_dict[article["type"]]["list_category"]
        ratio_category = types_dict[article["type"]]["ratio_category"]
        # ------------------------------------------------------------------------------
        article["created_at"] = format_date(article["created_at"])
        # ------------------------------------------------------------------------------
        for x in article["shops"]:
            article["shops"][x]["sell_price"] = format_float(
                article["shops"][x]["sell_price"]
            )
        # ------------------------------------------------------------------------------
        if article["volume"] == 0:
            article["volume"] = ""
        else:
            article["volume"] = format_float(article["volume"])
        # ------------------------------------------------------------------------------
        if article["alcohol_by_volume"] == 0:
            article["alcohol_by_volume"] = ""
        else:
            article["alcohol_by_volume"] = format_float(article["alcohol_by_volume"])
        # ------------------------------------------------------------------------------
        # PRICE
        article["taxfree_price"] = (
            article["buy_price"]
            + article["excise_duty"]
            + article["social_security_levy"]
        )
        article["taxfree_price"] = round(article["taxfree_price"], 4)
        # ------------------------------------------------------------------------------
        # PACKAGING
        if article["packaging"] == 0:
            article["packaging"] = ""
        # ------------------------------------------------------------------------------
        if article["deposit"]["unit"] == 0:
            article["deposit"]["unit"] = ""
        else:
            article["deposit"]["unit"] = format_float(article["deposit"]["unit"])

        if article["deposit"]["case"] == 0:
            article["deposit"]["case"] = ""
        else:
            article["deposit"]["case"] = format_float(article["deposit"]["case"])
        # ------------------------------------------------------------------------------
        article["list_category"] = list_category
    # ------------------------------------------------------------------------------
    return articles


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# FORMAT_ARTICLE_TO_DB
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def format_article_to_db(
    action, article, request_form, current_user, shops_margins, ratio_category
):
    formated_article = OrderedDict()
    # ------------------------------------------------------------------------------
    # 02 VALIDATED
    if action == "create":
        if current_user.role == Role.ADMIN:
            formated_article["validated"] = True
        else:
            formated_article["validated"] = False
    elif current_user.role == Role.ADMIN:
        formated_article["validated"] = True
    else:
        formated_article["validated"] = article["validated"]
    # ------------------------------------------------------------------------------
    # 03 CREATED_BY
    if action == "create":
        formated_article["created_by"] = current_user.name
    else:
        formated_article["created_by"] = article["created_by"]
    # ------------------------------------------------------------------------------
    # 04 CREATED_AT
    date = datetime.datetime.utcnow()
    if action == "create":
        formated_article["created_at"] = date
    else:
        formated_article["created_at"] = article["created_at"]
    # ------------------------------------------------------------------------------
    # 05 UPDATED_AT
    formated_article["updated_at"] = date
    # ------------------------------------------------------------------------------
    # 06 DISTRIBUTOR
    formated_article["distributor"] = request_form.get(
        "distributor", article.get("distributor", "")
    )
    # ------------------------------------------------------------------------------
    # 07 DISTRIBUTOR_REFERENCE
    formated_article["distributor_reference"] = request_form.get(
        "distributor_reference", article.get("distributor_reference", "")
    )
    # ------------------------------------------------------------------------------
    # 08 BARCODE
    formated_article["barcode"] = request_form.get(
        "barcode", article.get("barcode", "")
    )
    # ------------------------------------------------------------------------------
    # 09 REFERENCE
    formated_article["reference"] = request_form.get(
        "reference", article.get("reference", "")
    )
    # ------------------------------------------------------------------------------
    # 10 BUY_PRICE
    formated_article["buy_price"] = float(
        request_form.get("buy_price", article.get("buy_price", 0.0))
    )
    # ------------------------------------------------------------------------------
    # 11 EXCISE_DUTY
    if "excise_duty" in request_form:
        if request_form["excise_duty"] == "":
            formated_article["excise_duty"] = 0.0
        else:
            formated_article["excise_duty"] = float(request_form["excise_duty"])
    else:
        formated_article["excise_duty"] = article.get("excise_duty", 0.0)
    # ------------------------------------------------------------------------------
    # 12 SOCIAL_SECURITY_LEVY
    if "social_security_levy" in request_form:
        if request_form["social_security_levy"] == "":
            formated_article["social_security_levy"] = 0.0
        else:
            formated_article["social_security_levy"] = float(
                request_form["social_security_levy"]
            )
    else:
        formated_article["social_security_levy"] = article.get(
            "social_security_levy", 0.0
        )
    # ------------------------------------------------------------------------------
    # 13 TAX
    formated_article["tax"] = float(request_form.get("tax", article.get("tax", 0.0)))
    # ------------------------------------------------------------------------------
    # 14 SHOPS
    buy_price = formated_article["buy_price"]
    excise_duty = formated_article["excise_duty"]
    social_security_levy = formated_article["social_security_levy"]
    taxfree_price = buy_price + excise_duty + social_security_levy
    tax = formated_article["tax"]

    formated_article["shops"] = OrderedDict()
    for shop in [
        "angouleme",
        "sainte-eulalie",
        "pessac",
    ]:
        margins = shops_margins[shop]["margins"][ratio_category]
        temp = OrderedDict()
        if "sell_price_" + shop in request_form:
            temp["sell_price"] = float(request_form["sell_price_" + shop])
            temp["bar_price"] = float(request_form["bar_price_" + shop])
            temp["stock_quantity"] = int(request_form["stock_quantity_" + shop])
        else:
            if action == "create":
                # Si c'est une catégorie sans coeff, les prix de vente sont pris égaux au 1er du formulaire
                if ratio_category == "others":
                    temp["sell_price"] = float(
                        [v for (k, v) in request_form.items() if "sell_price_" in k][0]
                    )
                # Sinon on calcul le PVC
                else:
                    temp["sell_price"] = calculate_recommended_price(
                        taxfree_price, tax, ratio_category, margins
                    )
                temp["bar_price"] = 0.0
                temp["stock_quantity"] = 0
            elif action != "create":
                if (
                    buy_price != article["buy_price"]
                    or excise_duty != article["excise_duty"]
                    or social_security_levy != article["social_security_levy"]
                ):
                    old_taxfree_price = (
                        article["buy_price"]
                        + article["excise_duty"]
                        + article["social_security_levy"]
                    )
                    sell_price = article["shops"][shop]["sell_price"]
                    temp["sell_price"] = update_price(
                        old_taxfree_price,
                        taxfree_price,
                        tax,
                        sell_price,
                        ratio_category,
                        margins,
                    )
                else:
                    temp["sell_price"] = article["shops"][shop]["sell_price"]
                temp["bar_price"] = article["shops"][shop]["bar_price"]
                temp["stock_quantity"] = article["shops"][shop]["stock_quantity"]
        formated_article["shops"][shop] = temp
    # ------------------------------------------------------------------------------
    # 15 TYPE
    formated_article["type"] = request_form.get("type")
    # ------------------------------------------------------------------------------
    # 16 NAME
    formated_article["name"] = OrderedDict()
    for x in ["name1", "name2"]:
        if x in request_form:
            if request_form[x] == "-":
                formated_article["name"][x] = ""
            else:
                formated_article["name"][x] = request_form[x]
        else:
            if "name" in article:
                formated_article["name"][x] = article["name"][x]
            else:
                formated_article["name"][x] = ""
    # ------------------------------------------------------------------------------
    # 17 VOLUME
    if "volume" in request_form:
        if request_form["volume"] == "":
            formated_article["volume"] = 0.0
        else:
            formated_article["volume"] = float(request_form["volume"])
    else:
        formated_article["volume"] = article.get("volume", 0.0)
    # ------------------------------------------------------------------------------
    # 18 ALCOHOL_BY_VOLUME
    if "alcohol_by_volume" in request_form:
        if request_form["alcohol_by_volume"] == "":
            formated_article["alcohol_by_volume"] = 0.0
        else:
            formated_article["alcohol_by_volume"] = float(
                request_form["alcohol_by_volume"]
            )
    else:
        formated_article["alcohol_by_volume"] = article.get("alcohol_by_volume", 0.0)
    # ------------------------------------------------------------------------------
    # 19 REGION
    formated_article["region"] = request_form.get("region", article.get("region", ""))
    # ------------------------------------------------------------------------------
    # 20 COLOR
    formated_article["color"] = request_form.get("color", article.get("color", ""))
    # ------------------------------------------------------------------------------
    # 21 TASTE
    formated_article["taste"] = request_form.get("taste", article.get("taste", ""))
    if formated_article["taste"] == "-":
        formated_article["taste"] = ""
    # ------------------------------------------------------------------------------
    # 22 PACKAGING
    if "packaging" in request_form:
        if request_form["packaging"] == "":
            formated_article["packaging"] = 0
        else:
            formated_article["packaging"] = int(request_form["packaging"])
    else:
        formated_article["packaging"] = article.get("packaging", 0)
    # ------------------------------------------------------------------------------
    # 23 DEPOSIT
    formated_article["deposit"] = OrderedDict()
    for x in ["unit", "case"]:
        if x in request_form:
            if request_form[x] == "":
                formated_article["deposit"][x] = 0.0
            else:
                formated_article["deposit"][x] = float(request_form[x])
        else:
            if "deposit" in article:
                formated_article["deposit"][x] = article["deposit"][x]
            else:
                formated_article["deposit"][x] = 0.0
    # ------------------------------------------------------------------------------
    # 24 FOOD_PAIRING
    if "food_pairing_0" in request_form:
        food_pairing = [
            request_form.get(x)
            for x in request_form
            if "food_pairing_" in x and request_form.get(x) != "-"
        ]
    else:
        if "food_pairing" in article:
            food_pairing = article["food_pairing"]
        else:
            food_pairing = []
    formated_article["food_pairing"] = food_pairing
    # ------------------------------------------------------------------------------
    # 25 BIODYNAMIC
    formated_article["biodynamic"] = request_form.get(
        "biodynamic", article.get("biodynamic", "")
    )
    if formated_article["biodynamic"] == "-":
        formated_article["biodynamic"] = ""
    # ------------------------------------------------------------------------------
    return formated_article


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# TACTILL
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def format_volume(volume):
    if volume > 100:
        v = str(volume / 100).rstrip("0").rstrip(".")
        unit = "L"
    else:
        v = str(volume).rstrip("0").rstrip(".")
        unit = "cl"
    return f"{v}{unit}"


def define_tactill_name(article, list_category):
    name1 = article["name"]["name1"]
    name2 = article["name"]["name2"]
    volume = format_volume(article["volume"])
    color = article["color"]

    if list_category in {"beer", "cider"}:
        return f"{name2} {volume} {name1}".strip()

    elif list_category in {"keg", "mini_keg"}:
        if name1:
            return f"{name1} {name2} {volume}"
        else:
            return f"{name2} {volume}"

    elif list_category in {"rhum", "whisky", "spirit", "arranged", "sparkling_wine"}:
        if name1:
            return f"{name1} {name2} {volume}"
        else:
            return f"{name2} {volume}"

    elif list_category in {"bib", "wine", "fortified_wine"}:
        if name1:
            if name2:
                return f"{name2} {color} {volume} {name1}"
            else:
                return f"{name1} {color} {volume}"
        else:
            return f"{name2} {color} {volume}"

    elif list_category in {"box", "misc", "food"}:
        return f"{name1}"


def define_tactill_name2(name1, name2, volume, color, list_category):
    volume = format_volume(volume)

    if list_category in {"beer", "cider"}:
        return f"{name2} {volume} {name1}".strip()

    elif list_category in {"keg", "mini_keg"}:
        if name1:
            return f"{name1} {name2} {volume}"
        else:
            return f"{name2} {volume}"

    elif list_category in {"rhum", "whisky", "spirit", "arranged", "sparkling_wine"}:
        if name1:
            return f"{name1} {name2} {volume}"
        else:
            return f"{name2} {volume}"

    elif list_category in {"bib", "wine", "fortified_wine"}:
        if name1:
            if name2:
                return f"{name2} {color} {volume} {name1}"
            else:
                return f"{name1} {color} {volume}"
        else:
            return f"{name2} {color} {volume}"

    elif list_category in {"box", "misc", "food"}:
        return f"{name1}"


def define_tactill_icon_text(volume):
    if volume != 0:
        if volume > 100:
            return str(volume / 100).rstrip("0").rstrip(".").ljust(4)
        else:
            return str(volume).rstrip("0").rstrip(".").ljust(4)
    else:
        return "    "


def define_tactill_color(color, list_category):
    if list_category in {"beer", "cider", "keg", "mini_keg"}:
        if color == "Ambrée":
            return "#FF6347"
        elif color == "Blanche":
            return "#9EA09E"
        elif color == "Blonde":
            return "#F2BA43"
        elif color == "Brune":
            return "#A06E58"
        elif color == "Fruitée":
            return "#F44F60"

    elif list_category == "rhum":
        return "#30BEA5"

    elif list_category == "whisky":
        return "#1E8CFF"

    elif list_category in {"spirit", "arranged"}:
        return "#9EA09E"

    elif list_category in {"wine", "fortified_wine", "sparkling_wine", "bib"}:
        if color == "Blanc":
            return "#F2BA43"
        elif color == "Rosé":
            return "#B455C8"
        elif color == "Rouge":
            return "#F44F60"

    elif list_category == "box":
        return "#B455C8"

    elif list_category in {"misc", "food"}:
        return "#57DB47"
