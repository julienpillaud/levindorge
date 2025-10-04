import json
import math
from collections import defaultdict
from typing import Any

from app.domain.articles.entities import ArticleMargins
from app.domain.commons.entities import PricingGroup
from app.domain.shops.entities import ShopMargin

DECIMAL_ROUND_SWITCH = 0.1
SPIRIT_PRICE_RATIO_SWITCH = 100
SPIRIT_PRICE_BOOST = 10


def apply_rounding(value: float, decimal_round: float) -> float:
    factor = 1 / decimal_round
    if decimal_round < DECIMAL_ROUND_SWITCH:
        return math.ceil(value * factor) / factor
    return round(value * factor) / factor


def compute_recommended_price(
    net_price: float,
    tax_rate: float,
    shop_margins: ShopMargin,
    pricing_group: str,
) -> float:
    ratio = shop_margins.ratio
    if pricing_group == PricingGroup.SPIRIT and net_price >= SPIRIT_PRICE_RATIO_SWITCH:
        ratio += SPIRIT_PRICE_BOOST

    tax_factor = 1 + (tax_rate / 100)
    if shop_margins.operator == "+":
        price = (net_price + ratio) * tax_factor
    else:
        price = (net_price * ratio) * tax_factor

    return apply_rounding(value=price, decimal_round=shop_margins.decimal_round)


def compute_margin(net_price: float, tax_rate: float, gross_price: float) -> float:
    tax_factor = 1 + (tax_rate / 100)
    return (gross_price / tax_factor) - net_price


def compute_markup_rate(tax_rate: float, gross_price: float, margin: float) -> float:
    if gross_price == 0:
        return 0

    tax_factor = 1 + (tax_rate / 100)
    return margin / (gross_price / tax_factor) * 100


def compute_article_margins(
    net_price: float,
    tax_rate: float,
    gross_price: float,
) -> ArticleMargins:
    margin = compute_margin(
        net_price=net_price, tax_rate=tax_rate, gross_price=gross_price
    )
    markup = compute_markup_rate(
        tax_rate=tax_rate, gross_price=gross_price, margin=margin
    )
    return ArticleMargins(margin=round(margin, 2), markup=round(markup))


def extract_name(data: dict[str, Any]) -> None:
    data["name"] = {
        "name1": data.pop("name1", ""),
        "name2": data.pop("name2", ""),
    }


def extract_volume(data: dict[str, Any]) -> None:
    volume_data = data.pop("volume", None)

    try:
        volume = json.loads(volume_data)
        data["volume"] = volume
    except json.decoder.JSONDecodeError:
        data["volume"] = None


def extract_deposit(data: dict[str, Any]) -> None:
    data["deposit"] = {
        "unit": data.pop("unit", 0),
        "case": data.pop("case", 0),
    }


def extract_shops(data: dict[str, Any]) -> None:
    shops: dict[str, dict[str, Any]] = defaultdict(dict)

    for key, value in data.items():
        if "_price_" in key:
            field, _, shop = key.partition("_price_")
            shops[shop][f"{field}_price"] = float(value)
            shops[shop]["stock_quantity"] = 0

        elif key.startswith("margin_"):
            _, shop = key.split("_", 1)
            shops[shop].setdefault("margins", {})
            shops[shop]["margins"]["margin"] = float(value)
            shops[shop]["stock_quantity"] = 0

        elif key.startswith("profit_"):
            _, shop = key.split("_", 1)
            shops[shop].setdefault("margins", {})
            shops[shop]["margins"]["markup"] = float(value)
            shops[shop]["stock_quantity"] = 0

    data["shops"] = shops
