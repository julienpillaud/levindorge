from typing import Any

from bson import ObjectId
from cleanstack.exceptions import NotFoundError
from cleanstack.infrastructure.mongodb.types import MongoDocument
from pymongo.client_session import ClientSession
from pymongo.database import Database

from app.domain.entities import (
    DomainEntity,
    EntityId,
    PaginatedResponse,
    Pagination,
    SortEntity,
)
from app.domain.filters import FilterEntity
from app.domain.protocols.repository import RepositoryProtocol
from app.infrastructure.repository.exceptions import MongoRepositoryError
from app.infrastructure.repository.utils import PipelineBuilder
from app.infrastructure.utils import iter_dicts


class MongoRepository[T: DomainEntity](RepositoryProtocol[T]):
    domain_entity_type: type[T]
    collection_name: str
    searchable_fields: tuple[str, ...]

    def __init__(
        self,
        database: Database[MongoDocument],
        session: ClientSession | None = None,
    ):
        self.database = database
        self.collection = self.database[self.collection_name]
        self.session = session

    def get_all(
        self,
        filters: list[FilterEntity] | None = None,
        search: str | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[T]:
        pagination = pagination or Pagination()

        pipeline = (
            PipelineBuilder()
            .add_search(search, self.searchable_fields)
            .add_filters(filters)
            .add_lookups(self._lookups)
            .add_sort(sort)
            .add_pagination(pagination)
        )

        count_result = list(self.collection.aggregate(pipeline.count))
        total = count_result[0]["total"] if count_result else 0

        data_result = self.collection.aggregate(pipeline.data)

        return PaginatedResponse(
            page=pagination.page,
            limit=pagination.limit,
            total=total,
            total_pages=(total + pagination.limit - 1) // pagination.limit,
            items=[self._to_domain_entity(item) for item in data_result],
        )

    def get_one(self, filters: dict[str, Any] | None = None) -> T | None:
        pipeline = []
        if filters:
            pipeline.extend([{"$match": filters}])
        pipeline.extend(self._lookups)

        result = next(self.collection.aggregate(pipeline, session=self.session), None)
        return self._to_domain_entity(result) if result else None

    def get_by_id(self, entity_id: EntityId, /) -> T | None:
        result = self._get_by_id(entity_id)
        return self._to_domain_entity(result) if result else None

    def create(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)

        result = self.collection.insert_one(db_entity, session=self.session)

        db_result = self._get_by_id(result.inserted_id)
        if not db_result:
            raise NotFoundError("Entity not found.")

        return self._to_domain_entity(db_result)

    def create_many(self, entities: list[T], /) -> list[EntityId]:
        db_entities = [self._to_database_entity(entity) for entity in entities]

        result = self.collection.insert_many(db_entities, session=self.session)

        return [str(entity) for entity in result.inserted_ids]

    def update(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)

        result = self.collection.replace_one(
            {"_id": ObjectId(entity.id)},
            db_entity,
            session=self.session,
        )
        if not result.modified_count:
            raise MongoRepositoryError()

        db_result = self._get_by_id(entity.id)
        if not db_result:
            raise NotFoundError("Entity not found.")

        return self._to_domain_entity(db_result)

    def delete(self, entity: T, /) -> None:
        self.collection.delete_one({"_id": ObjectId(entity.id)}, session=self.session)

    def _get_by_id(self, entity_id: EntityId, /) -> MongoDocument | None:
        pipeline = [
            {"$match": {"_id": ObjectId(entity_id)}},
            *self._lookups,
        ]
        return next(self.collection.aggregate(pipeline, session=self.session), None)

    def _to_domain_entity(self, document: MongoDocument, /) -> T:
        self._normalize_ids(document)
        return self.domain_entity_type.model_validate(document)

    @staticmethod
    def _to_database_entity(entity: T, /) -> MongoDocument:
        return entity.model_dump(exclude={"id"})

    @property
    def _lookups(self) -> list[MongoDocument]:
        return []

    @staticmethod
    def _normalize_ids(document: MongoDocument, /) -> None:
        for d in iter_dicts(document):
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
