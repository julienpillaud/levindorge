from typing import Any

from bson import ObjectId
from cleanstack.exceptions import NotFoundError
from pymongo.database import Database

from app.domain.entities import (
    DomainEntity,
    EntityId,
    PaginatedResponse,
    Pagination,
    QueryParams,
)
from app.domain.filters import FilterEntity, FilterOperator
from app.domain.protocols.repository import RepositoryProtocol
from app.infrastructure.repository.exceptions import MongoRepositoryError
from app.infrastructure.utils import iter_dicts

type MongoDocument = dict[str, Any]


class MongoRepository[T: DomainEntity](RepositoryProtocol[T]):
    domain_entity_type: type[T]
    collection_name: str
    searchable_fields: tuple[str, ...]

    def __init__(self, database: Database[MongoDocument]):
        self.database = database
        self.collection = self.database[self.collection_name]

    def get_all(
        self,
        query: QueryParams | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[T]:
        query = query or QueryParams()
        pagination = pagination or Pagination()

        pipeline = []

        if query.filters:
            mongo_filters = self._build_match_stage(query.filters)
            pipeline.append({"$match": mongo_filters})

        if query.search:
            pipeline.extend(self._search_pipeline(query.search))
        pipeline.extend(self._aggregation_pipeline())
        if query.sort:
            pipeline.append({"$sort": query.sort})
        facet_pipeline = [
            *pipeline,
            {
                "$facet": {
                    "metadata": [{"$count": "total"}],
                    "data": [{"$skip": pagination.skip}, {"$limit": pagination.limit}],
                }
            },
        ]

        result = list(self.collection.aggregate(facet_pipeline))
        total = result[0]["metadata"][0]["total"] if result[0]["metadata"] else 0
        items_db = result[0]["data"]

        return PaginatedResponse(
            page=pagination.page,
            limit=pagination.limit,
            total=total,
            total_pages=(total + pagination.limit - 1) // pagination.limit,
            items=[self._to_domain_entity(item) for item in items_db],
        )

    def get_one(self, filters: dict[str, Any] | None = None) -> T | None:
        pipeline = []
        if filters:
            pipeline.extend([{"$match": filters}])
        pipeline.extend(self._aggregation_pipeline())

        result = next(self.collection.aggregate(pipeline), None)
        return self._to_domain_entity(result) if result else None

    def get_by_id(self, entity_id: EntityId, /) -> T | None:
        result = self._get_by_id(entity_id)
        return self._to_domain_entity(result) if result else None

    def create(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)

        result = self.collection.insert_one(db_entity)

        db_result = self._get_by_id(result.inserted_id)
        if not db_result:
            raise NotFoundError("Entity not found.")

        return self._to_domain_entity(db_result)

    def create_many(self, entities: list[T], /) -> list[EntityId]:
        db_entities = [self._to_database_entity(entity) for entity in entities]

        result = self.collection.insert_many(db_entities)

        return [str(entity) for entity in result.inserted_ids]

    def update(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)

        result = self.collection.replace_one({"_id": ObjectId(entity.id)}, db_entity)
        if not result.modified_count:
            raise MongoRepositoryError()

        db_result = self._get_by_id(entity.id)
        if not db_result:
            raise NotFoundError("Entity not found.")

        return self._to_domain_entity(db_result)

    def delete(self, entity: T, /) -> None:
        self.collection.delete_one({"_id": ObjectId(entity.id)})

    def _get_by_id(self, entity_id: str, /) -> MongoDocument | None:
        pipeline = [
            {"$match": {"_id": ObjectId(entity_id)}},
            *self._aggregation_pipeline(),
        ]
        return next(self.collection.aggregate(pipeline), None)

    def _to_domain_entity(self, document: MongoDocument, /) -> T:
        self._normalize_ids(document)
        return self.domain_entity_type.model_validate(document)

    @staticmethod
    def _to_database_entity(entity: T, /) -> MongoDocument:
        return entity.model_dump(exclude={"id"})

    def _search_pipeline(self, search: str, /) -> list[MongoDocument]:
        conditions = [
            {field: {"$regex": search.strip(), "$options": "i"}}
            for field in self.searchable_fields
        ]
        return [{"$match": {"$or": conditions}}]

    @staticmethod
    def _aggregation_pipeline() -> list[MongoDocument]:
        return []

    @staticmethod
    def _normalize_ids(document: MongoDocument, /) -> None:
        for d in iter_dicts(document):
            if "_id" in d:
                d["id"] = str(d.pop("_id"))

    @staticmethod
    def _build_match_stage(filters: list[FilterEntity]) -> dict[str, Any]:
        match_query = {}

        for filter_ in filters:
            match filter_.operator:
                case FilterOperator.EQ:
                    match_query[filter_.field] = filter_.value

        return match_query
