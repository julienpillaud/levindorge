from typing import Any

from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.collection import Collection

from app.domain.entities import DomainEntity


class BaseFactory[T: DomainEntity]:
    def create_one(self, **kwargs: Any) -> T:
        entity = self.build_entity(**kwargs)
        return self._insert_one(entity)

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:
        entities = [self.build_entity(**kwargs) for _ in range(count)]
        return self._insert_many(entities)

    def build_entity(self, **kwargs: Any) -> T:
        """Build a domain entity with the given kwargs."""
        raise NotImplementedError()

    def _insert_one(self, entity: T) -> T:
        """Insert a single entity into the database."""
        raise NotImplementedError()

    def _insert_many(self, entities: list[T]) -> list[T]:
        """Insert multiple entities into the database."""
        results: list[T] = []
        for entity in entities:
            result = self._insert_one(entity)
            results.append(result)
        return results


class MongoBaseFactory[T: DomainEntity](BaseFactory[T]):
    domain_entity_type: type[T]

    def __init__(self, collection: Collection[MongoDocument]):
        self.collection = collection

    def _insert_one(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)
        result = self.collection.insert_one(db_entity)
        db_result = self.collection.find_one({"_id": result.inserted_id})
        if not db_result:
            raise RuntimeError()
        return self._to_domain_entity(db_entity)

    def _to_database_entity(self, entity: T, /) -> MongoDocument:
        return entity.model_dump(exclude={"id"})

    def _to_domain_entity(self, document: MongoDocument, /) -> T:
        document["id"] = str(document.pop("_id"))
        return self.domain_entity_type.model_validate(document)
