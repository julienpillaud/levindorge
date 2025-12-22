from typing import Any

from polyfactory.factories.pydantic_factory import ModelFactory

from app.domain.origins.entities import Origin
from app.infrastructure.repository.origins import OriginRepository
from tests.factories.base import BaseMongoFactory


class OriginEntityFactory(ModelFactory[Origin]): ...


class OriginFactory(BaseMongoFactory[Origin]):
    repository_class = OriginRepository

    def build(self, **kwargs: Any) -> Origin:
        return OriginEntityFactory.build(**kwargs)
