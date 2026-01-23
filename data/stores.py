from decimal import Decimal

from app.domain.commons.entities import PricingGroup
from app.domain.stores.entities import PricingConfig, RoundConfig, RoundingMode

PRICING_CONFIG = {
    PricingGroup.BEER: PricingConfig(
        value=Decimal("1.7"),
        operator="*",
        round_config=RoundConfig(
            value=Decimal("0.05"),
            rounding_mode=RoundingMode.ROUND_CEILING,
        ),
    ),
    PricingGroup.KEG: PricingConfig(
        value=Decimal("32.5"),
        operator="+",
        round_config=RoundConfig(
            value=Decimal("1"),
            rounding_mode=RoundingMode.ROUND_HALF_EVEN,
        ),
    ),
    PricingGroup.MINI_KEG: PricingConfig(
        value=Decimal("5"),
        operator="+",
        round_config=RoundConfig(
            value=Decimal("1"),
            rounding_mode=RoundingMode.ROUND_HALF_EVEN,
        ),
    ),
    PricingGroup.SPIRIT: PricingConfig(
        value=Decimal("10"),
        operator="+",
        round_config=RoundConfig(
            value=Decimal("1"),
            rounding_mode=RoundingMode.ROUND_HALF_EVEN,
        ),
    ),
    PricingGroup.ARRANGED: PricingConfig(
        value=Decimal("5"),
        operator="+",
        round_config=RoundConfig(
            value=Decimal("1"),
            rounding_mode=RoundingMode.ROUND_HALF_EVEN,
        ),
    ),
    PricingGroup.WINE: PricingConfig(
        value=Decimal("1.5"),
        operator="*",
        round_config=RoundConfig(
            value=Decimal("0.05"),
            rounding_mode=RoundingMode.ROUND_CEILING,
        ),
    ),
    PricingGroup.BIB: PricingConfig(
        value=Decimal("5"),
        operator="+",
        round_config=RoundConfig(
            value=Decimal("1"),
            rounding_mode=RoundingMode.ROUND_HALF_EVEN,
        ),
    ),
    PricingGroup.BOX: PricingConfig(
        value=Decimal("1.5"),
        operator="*",
        round_config=RoundConfig(
            value=Decimal("1"),
            rounding_mode=RoundingMode.ROUND_HALF_EVEN,
        ),
    ),
    PricingGroup.OTHER: PricingConfig(
        value=Decimal("1.06"),
        operator="*",
        round_config=RoundConfig(
            value=Decimal("0.05"),
            rounding_mode=RoundingMode.ROUND_CEILING,
        ),
    ),
}
