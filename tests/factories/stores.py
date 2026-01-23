from typing import Any

from faker import Faker

from app.domain.stores.entities import Store
from app.infrastructure.repository.stores import StoreRepository
from data.stores import PRICING_CONFIG
from tests.factories.base import BaseMongoFactory


def generate_store(faker: Faker, **kwargs: Any) -> Store:
    return Store(
        name=kwargs["name"] if "name" in kwargs else faker.word(),
        slug=kwargs["slug"] if "slug" in kwargs else faker.slug(),
        tactill_api_key=kwargs["tactill_api_key"]
        if "tactill_api_key" in kwargs
        else faker.uuid4(),
        pricing_configs=PRICING_CONFIG,
    )


class StoreFactory(BaseMongoFactory[Store]):
    repository_class = StoreRepository

    def build(self, **kwargs: Any) -> Store:
        return generate_store(self.faker, **kwargs)
