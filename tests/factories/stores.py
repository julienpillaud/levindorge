from typing import Any, ClassVar

from polyfactory.factories.pydantic_factory import ModelFactory

from app.domain.commons.entities import PricingGroup
from app.domain.stores.entities import PricingConfig, Store
from app.infrastructure.repository.stores import StoreRepository
from tests.factories.base import BaseMongoFactory


class PricingConfigEntityFactory(ModelFactory[PricingConfig]): ...


class StoreEntityFactory(ModelFactory[Store]):
    pricing_configs: ClassVar[dict[PricingGroup, PricingConfig]] = {
        group: PricingConfigEntityFactory.build() for group in PricingGroup
    }


class StoreFactory(BaseMongoFactory[Store]):
    repository_class = StoreRepository

    def build(self, **kwargs: Any) -> Store:
        return StoreEntityFactory.build(**kwargs)
