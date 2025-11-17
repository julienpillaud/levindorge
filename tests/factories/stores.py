from typing import Any, ClassVar

from polyfactory.factories.pydantic_factory import ModelFactory

from app.domain.commons.entities import PricingGroup
from app.domain.stores.entities import PricingConfig, Store
from tests.factories.base import MongoBaseFactory


class PricingConfigEntityFactory(ModelFactory[PricingConfig]): ...


class StoreEntityFactory(ModelFactory[Store]):
    pricing_configs: ClassVar[dict[PricingGroup, PricingConfig]] = {
        group: PricingConfigEntityFactory.build() for group in PricingGroup
    }


class StoreFactory(MongoBaseFactory[Store]):
    domain_entity_type = Store

    def build_entity(self, **kwargs: Any) -> Store:
        return StoreEntityFactory.build(**kwargs)
