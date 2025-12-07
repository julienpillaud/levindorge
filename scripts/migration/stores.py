from decimal import Decimal
from typing import Any

from rich import print

from app.core.core import Context
from app.domain.commons.entities import PricingGroup
from app.domain.stores.entities import PricingConfig, RoundConfig, RoundingMode, Store


def create_stores(src_context: Context, dst_context: Context) -> list[Store]:
    # Get previous stores
    src_stores = list(src_context.database["shops"].find())
    # Create stores with the new entity model
    dst_stores = create_store_entities(src_stores)

    # Save stores in the database
    result = dst_context.store_repository.create_many(dst_stores)
    count = len(result)
    print(f"Created {count} stores ({len(src_stores)})")
    return dst_context.store_repository.get_all(limit=count).items


def create_store_entities(src_stores: list[dict[str, Any]]) -> list[Store]:
    return [
        Store(
            name=store["name"],
            slug=store["username"],
            tactill_api_key=store["tactill_api_key"],
            pricing_configs=PRICING_CONFIG,
        )
        for store in src_stores
    ]


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
