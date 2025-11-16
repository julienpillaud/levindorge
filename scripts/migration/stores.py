from app.core.core import Context
from app.domain.commons.entities import PricingGroup
from app.domain.stores.entities import PricingConfig, Store


def update_stores(src_context: Context, dst_context: Context) -> None:
    src_stores = src_context.database["shops"].find()
    dst_stores = [
        Store(
            name=store["name"],
            slug=store["username"],
            tactill_api_key=store["tactill_api_key"],
            pricing_configs={
                pricing_group: PricingConfig(
                    value=store["margins"][pricing_group]["ratio"],
                    operator=store["margins"][pricing_group]["operator"],
                    round_step=store["margins"][pricing_group]["decimal_round"],
                )
                for pricing_group in PricingGroup
            },
        )
        for store in src_stores
    ]

    dst_context.store_repository.create_many(dst_stores)
