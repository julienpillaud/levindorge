from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.database import Database

from app.domain.commons.entities import PricingGroup
from app.domain.stores.entities import PricingConfig, Store


def update_stores(
    src_database: Database[MongoDocument],
    dst_database: Database[MongoDocument],
) -> None:
    dst_stores: list[MongoDocument] = []
    for src_store in src_database["shops"].find():
        dst_store = Store(
            name=src_store["name"],
            slug=src_store["username"],
            tactill_api_key=src_store["tactill_api_key"],
            pricing_configs={
                pricing_group: PricingConfig(
                    value=src_store["margins"][pricing_group]["ratio"],
                    operator=src_store["margins"][pricing_group]["operator"],
                    round_step=src_store["margins"][pricing_group]["decimal_round"],
                )
                for pricing_group in PricingGroup
            },
        )
        dst_stores.append(dst_store.model_dump(exclude={"id"}))

    dst_database["stores"].insert_many(dst_stores)
