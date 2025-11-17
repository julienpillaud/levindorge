from typing import Any, ClassVar

from polyfactory.factories.pydantic_factory import ModelFactory

from app.domain.stores.entities import Store
from app.domain.users.entities import User
from app.infrastructure.repository.users import UserRepository
from tests.factories.base import BaseFactory
from tests.factories.stores import StoreFactory


class UserEntityFactory(ModelFactory[User]):
    # Should not create stores who are not persists
    stores: ClassVar[list[Store]] = []


class UserFactory(BaseFactory[User]):
    @property
    def repository(self) -> UserRepository:
        return UserRepository(database=self.database)

    @property
    def store_factory(self) -> StoreFactory:
        return StoreFactory(database=self.database)

    def build(self, **kwargs: Any) -> User:
        if "stores" not in kwargs:
            kwargs["stores"] = [self.store_factory.create_one()]
        return UserEntityFactory.build(**kwargs)
