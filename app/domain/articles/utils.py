from decimal import Decimal

from app.domain.articles.entities import ArticleMargins
from app.domain.commons.entities import PricingGroup
from app.domain.stores.entities import PricingConfig, RoundConfig

SPIRIT_PRICE_THRESHOLD = 100
SPIRIT_EXTRA_MARGIN = 10


def apply_rounding(value: Decimal, round_config: RoundConfig) -> Decimal:
    ratio = value / round_config.value
    rounded_ratio = ratio.quantize(
        Decimal("1"),
        # mypy do not consider pydantic 'use_enum_values' config
        rounding=round_config.rounding_mode,  # type: ignore
    )
    return rounded_ratio * round_config.value


def compute_recommended_price(
    total_cost: Decimal,
    vat_rate: Decimal,
    pricing_group: PricingGroup,
    pricing_config: PricingConfig,
) -> Decimal:
    value = pricing_config.value
    if pricing_group == PricingGroup.SPIRIT and total_cost >= SPIRIT_PRICE_THRESHOLD:
        value += SPIRIT_EXTRA_MARGIN

    vat_factor = 1 + (vat_rate / 100)
    if pricing_config.operator == "+":
        price = (total_cost + value) * vat_factor
    else:
        price = (total_cost * value) * vat_factor

    return apply_rounding(value=price, round_config=pricing_config.round_config)


def compute_margin_amount(
    total_cost: Decimal,
    vat_rate: Decimal,
    gross_price: Decimal,
) -> Decimal:
    tax_factor = 1 + (vat_rate / 100)
    return (gross_price / tax_factor) - total_cost


def compute_margin_rate(
    vat_rate: Decimal,
    gross_price: Decimal,
    margin_amount: Decimal,
) -> Decimal:
    if gross_price == 0:
        return Decimal("0")

    tax_factor = 1 + (vat_rate / 100)
    return margin_amount / (gross_price / tax_factor) * 100


def compute_article_margins(
    total_cost: Decimal,
    vat_rate: Decimal,
    gross_price: Decimal,
) -> ArticleMargins:
    margin_amount = compute_margin_amount(
        total_cost=total_cost,
        vat_rate=vat_rate,
        gross_price=gross_price,
    )
    margin_rate = compute_margin_rate(
        vat_rate=vat_rate,
        gross_price=gross_price,
        margin_amount=margin_amount,
    )
    return ArticleMargins(
        margin_amount=margin_amount.quantize(Decimal("1.00")),
        margin_rate=margin_rate.quantize(Decimal("1")),
    )


# def extract_deposit(data: dict[str, Any], key: str) -> float | None:
#     value = data.pop(key, None)
#     if not value:
#         return None
#     return float(value)
