import math

from application.entities.article import ArticleMargin
from application.entities.shop import ShopMargin


def compute_recommended_price(
    taxfree_price: float,
    tax: float,
    shop_margins: ShopMargin,
    ratio_category: str,
) -> float:
    if ratio_category == "spirit" and taxfree_price >= 100:
        shop_margins.ratio += 10

    if shop_margins.operator == "+":
        price = (taxfree_price + shop_margins.ratio) * (1 + tax / 100)
    else:
        price = (taxfree_price * shop_margins.ratio) * (1 + tax / 100)

    if shop_margins.decimal_round < 0.1:
        return math.ceil(price * (1 / shop_margins.decimal_round)) / (
            1 / shop_margins.decimal_round
        )

    return round(price * (1 / shop_margins.decimal_round)) / (
        1 / shop_margins.decimal_round
    )


def compute_article_margin(
    taxfree_price: float, tax: float, sell_price: float
) -> ArticleMargin:
    margin = compute_margin(taxfree_price=taxfree_price, tax=tax, sell_price=sell_price)
    markup = compute_markup(tax=tax, sell_price=sell_price, margin=margin)
    return ArticleMargin(margin=round(margin, 2), markup=round(markup))


def compute_margin(taxfree_price: float, tax: float, sell_price: float) -> float:
    tax_factor = 1 + (tax / 100)
    return (sell_price / tax_factor) - taxfree_price


def compute_markup(tax: float, sell_price: float, margin: float) -> float:
    if sell_price == 0:
        return 0
    tax_factor = 1 + (tax / 100)
    return margin / (sell_price / tax_factor) * 100
