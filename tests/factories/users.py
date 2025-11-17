from typing import Any, ClassVar

from cleanstack.infrastructure.mongo.entities import MongoDocument
from polyfactory.factories.pydantic_factory import ModelFactory

from app.domain.stores.entities import Store
from app.domain.users.entities import User
from tests.factories.base import MongoBaseFactory
from tests.factories.stores import StoreFactory


class UserEntityFactory(ModelFactory[User]):
    # Should not create stores who are not persists
    stores: ClassVar[list[Store]] = []


class UserFactory(MongoBaseFactory[User]):
    domain_entity_type = User
    collection_name = "users"

    @property
    def store_factory(self) -> StoreFactory:
        return StoreFactory(database=self.database)

    def build_entity(self, **kwargs: Any) -> User:
        if "stores" not in kwargs:
            kwargs["stores"] = [self.store_factory.create_one()]
        return UserEntityFactory.build(**kwargs)

    @staticmethod
    def _to_database_entity(entity: User, /) -> MongoDocument:
        document = entity.model_dump(exclude={"id"})
        document["stores"] = [store.slug for store in entity.stores]
        return document
