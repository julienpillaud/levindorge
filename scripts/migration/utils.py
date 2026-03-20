from cleanstack.entities import DomainEntity
from cleanstack.infrastructure.mongo.types import MongoDocument


def to_database_entity[T: DomainEntity](entity: T, /) -> MongoDocument:
    document = entity.model_dump(exclude={"id"})
    document["_id"] = entity.id
    return document
