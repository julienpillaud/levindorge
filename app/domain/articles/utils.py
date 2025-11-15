import json
import math
from collections import defaultdict
from typing import Any

from app.domain.articles.entities import ArticleMargins
from app.domain.commons.entities import PricingGroup
from app.domain.stores.entities import PricingConfig

SPIRIT_PRICE_THRESHOLD = 100
SPIRIT_EXTRA_MARGIN = 10
ROUND_STEP_CEIL_THRESHOLD = 0.1


def apply_rounding(value: float, round_step: float) -> float:
    factor = 1 / round_step
    if round_step < ROUND_STEP_CEIL_THRESHOLD:
        return math.ceil(value * factor) / factor
    return round(value * factor) / factor


def compute_recommended_price(
    total_cost: float,
    vat_rate: float,
    pricing_group: PricingGroup,
    pricing_config: PricingConfig,
) -> float:
    value = pricing_config.value
    if pricing_group == PricingGroup.SPIRIT and total_cost >= SPIRIT_PRICE_THRESHOLD:
        value += SPIRIT_EXTRA_MARGIN

    vat_factor = 1 + (vat_rate / 100)
    if pricing_config.operator == "+":
        price = (total_cost + value) * vat_factor
    else:
        price = (total_cost * value) * vat_factor

    return apply_rounding(value=price, round_step=pricing_config.round_step)


def compute_margin_amount(
    total_cost: float,
    vat_rate: float,
    gross_price: float,
) -> float:
    tax_factor = 1 + (vat_rate / 100)
    margin_amount = (gross_price / tax_factor) - total_cost
    return round(margin_amount, 2)


def compute_margin_rate(
    vat_rate: float,
    gross_price: float,
    margin_amount: float,
) -> float:
    if gross_price == 0:
        return 0

    tax_factor = 1 + (vat_rate / 100)
    margin_rate = margin_amount / (gross_price / tax_factor) * 100
    return round(margin_rate)


def compute_article_margins(
    total_cost: float,
    tax_rate: float,
    gross_price: float,
) -> ArticleMargins:
    margin_amount = compute_margin_amount(
        total_cost=total_cost,
        vat_rate=tax_rate,
        gross_price=gross_price,
    )
    margin_rate = compute_margin_rate(
        vat_rate=tax_rate,
        gross_price=gross_price,
        margin_amount=margin_amount,
    )
    return ArticleMargins(margin_amount=margin_amount, margin_rate=margin_rate)


def extract_name(data: dict[str, Any]) -> None:
    data["name"] = {
        "name1": data.pop("name1", ""),
        "name2": data.pop("name2", ""),
    }


def extract_volume(data: dict[str, Any]) -> None:
    volume_data = data.pop("volume", None)
    if not volume_data:
        data["volume"] = None
        return

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
