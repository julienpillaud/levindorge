import random
from typing import Any, cast

from faker import Faker

from app.domain.origins.entities import Origin, OriginType
from app.infrastructure.repository.origins import OriginRepository
from tests.factories.base import BaseMongoFactory


def generate_origin(faker: Faker, **kwargs: Any) -> Origin:
    origin_type = cast(
        OriginType,
        kwargs["type"] if "type" in kwargs else random.choice(list(OriginType)),
    )
    match origin_type:
        case OriginType.REGION:
            name = kwargs["name"] if "name" in kwargs else faker.region()
            code = None
        case OriginType.COUNTRY:
            name = kwargs["name"] if "name" in kwargs else faker.country()
            code = kwargs["code"] if "code" in kwargs else faker.country_code()

    return Origin(name=name, code=code, type=origin_type)


class OriginFactory(BaseMongoFactory[Origin]):
    repository_class = OriginRepository

    def build(self, **kwargs: Any) -> Origin:
        return generate_origin(self.faker, **kwargs)
