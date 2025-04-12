import math
import operator

from app.domain.articles.entities import Article, ArticleMargin
from app.domain.shops.entities import Shop

SPIRIT_PRICE_RATIO_SWITCH = 100
DECIMAL_ROUND_SWITCH = 0.1


def compute_recommended_price(article: Article, shop: Shop) -> float:
    ratio_category = article.type_infos.ratio_category
    margin = shop.margins[ratio_category]
    price_operator = operator.add if margin.operator == "+" else operator.mul

    if (
        ratio_category == "spirit"
        and article.taxfree_price >= SPIRIT_PRICE_RATIO_SWITCH
    ):
        margin.ratio += 10

    price = price_operator(article.taxfree_price, margin.ratio) * (
        1 + article.tax / 100
    )

    return round_price(price=price, decimal_round=margin.decimal_round)


def round_price(price: float, decimal_round: float) -> float:
    factor = 1 / decimal_round
    if decimal_round < DECIMAL_ROUND_SWITCH:
        return math.ceil(price * factor) / factor
    return round(price * factor) / factor


def compute_article_margin(article: Article, shop: Shop) -> ArticleMargin:
    sell_price = article.shops[shop.username].sell_price

    margin = compute_margin(article=article, sell_price=sell_price)
    markup = compute_markup(article=article, sell_price=sell_price, margin=margin)

    return ArticleMargin(margin=round(margin, 2), markup=round(markup))


def compute_margin(article: Article, sell_price: float) -> float:
    factor = 1 + (article.tax / 100)
    return (sell_price / factor) - article.taxfree_price


def compute_markup(article: Article, sell_price: float, margin: float) -> float:
    return (
        0
        if sell_price == 0
        else margin / (sell_price / (1 + (article.tax / 100))) * 100
    )
