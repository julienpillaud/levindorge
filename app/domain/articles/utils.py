import math
import operator

from app.domain.articles.entities import ArticleMargin
from app.domain.shops.entities import Shop

SPIRIT_PRICE_RATIO_SWITCH = 100
DECIMAL_ROUND_SWITCH = 0.1


def compute_recommended_price(
    ratio_category: str,
    taxfree_price: float,
    tax: float,
    shop: Shop,
) -> float:
    margin = shop.margins[ratio_category]
    price_operator = operator.add if margin.operator == "+" else operator.mul

    if ratio_category == "spirit" and taxfree_price >= SPIRIT_PRICE_RATIO_SWITCH:
        margin.ratio += 10

    price = price_operator(taxfree_price, margin.ratio) * (1 + tax / 100)

    return round_price(price=price, decimal_round=margin.decimal_round)


def round_price(price: float, decimal_round: float) -> float:
    factor = 1 / decimal_round
    if decimal_round < DECIMAL_ROUND_SWITCH:
        return math.ceil(price * factor) / factor
    return round(price * factor) / factor


def compute_article_margins(
    taxfree_price: float,
    tax: float,
    sell_price: float,
) -> ArticleMargin:
    margin = compute_margin(
        taxfree_price=taxfree_price,
        tax=tax,
        sell_price=sell_price,
    )
    markup = compute_markup(
        tax=tax,
        sell_price=sell_price,
        margin=margin,
    )

    return ArticleMargin(margin=round(margin, 2), markup=round(markup))


def compute_margin(taxfree_price: float, tax: float, sell_price: float) -> float:
    factor = 1 + (tax / 100)
    return (sell_price / factor) - taxfree_price


def compute_markup(tax: float, sell_price: float, margin: float) -> float:
    return 0 if sell_price == 0 else margin / (sell_price / (1 + (tax / 100))) * 100
