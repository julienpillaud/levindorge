from decimal import Decimal
from typing import Any

from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory

from app.domain.commons.entities import PricingGroup
from app.domain.stores.entities import PricingConfig, RoundConfig, RoundingMode, Store
from app.infrastructure.repository.stores import StoreRepository
from tests.factories.base import BaseMongoFactory


class StoreEntityFactory(ModelFactory[Store]):
    # return only one PricingGroup: polyfactory do not handle Decimal correctly
    pricing_configs = Use(
        lambda: {
            PricingGroup.BEER: PricingConfig(
                value=Decimal("1.7"),
                operator="*",
                round_config=RoundConfig(
                    value=Decimal("0.05"),
                    rounding_mode=RoundingMode.ROUND_CEILING,
                ),
            )
        }
    )


class StoreFactory(BaseMongoFactory[Store]):
    repository_class = StoreRepository

    def build(self, **kwargs: Any) -> Store:
        return StoreEntityFactory.build(**kwargs)
