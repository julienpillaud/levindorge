from typing import Any

from bson import ObjectId
from cleanstack.exceptions import NotFoundError
from cleanstack.infrastructure.mongo.entities import MongoDocument
from pydantic import PositiveInt
from pymongo.database import Database

from app.domain.entities import (
    DEFAULT_PAGINATION_SIZE,
    DomainModel,
    PaginatedResponse,
)
from app.domain.protocols.base_repository import RepositoryProtocol
from app.infrastructure.repository.exceptions import MongoRepositoryError


class MongoRepository[T: DomainModel](RepositoryProtocol[T]):
    domain_model: type[T]
    collection_name: str
    searchable_fields: tuple[str, ...]

    def __init__(self, database: Database[MongoDocument]):
        self.database = database
        self.collection = self.database[self.collection_name]

    def get_all(
        self,
        filters: dict[str, Any] | None = None,
        search: str | None = None,
        sort: dict[str, int] | None = None,
        page: PositiveInt = 1,
        limit: PositiveInt = DEFAULT_PAGINATION_SIZE,
    ) -> PaginatedResponse[T]:
        skip = (page - 1) * limit

        pipeline = []
        if filters:
            pipeline.extend([{"$match": filters}])
        if search:
            pipeline.extend(self._search_pipeline(search.strip()))
        pipeline.extend(self._aggregation_pipeline())
        if sort:
            pipeline.append({"$sort": sort})
        facet_pipeline = [
            *pipeline,
            {
                "$facet": {
                    "metadata": [{"$count": "total"}],
                    "data": [{"$skip": skip}, {"$limit": limit}],
                }
            },
        ]

        result = list(self.collection.aggregate(facet_pipeline))
        total = result[0]["metadata"][0]["total"] if result[0]["metadata"] else 0
        items_db = result[0]["data"]

        return PaginatedResponse(
            page=page,
            limit=limit,
            total=total,
            total_pages=(total + limit - 1) // limit,
            items=[self._to_domain_entity(item) for item in items_db],
        )

    def get_by_id(self, entity_id: str, /) -> T | None:
        result = self._get_database_entity(entity_id)
        return self._to_domain_entity(result) if result else None

    def create(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)

        result = self.collection.insert_one(db_entity)

        db_result = self._get_database_entity(result.inserted_id)
        if not db_result:
            raise NotFoundError()

        return self._to_domain_entity(db_result)

    def update(self, entity: T, /) -> T:
        db_entity = self._to_database_entity(entity)

        result = self.collection.replace_one({"_id": entity.id}, db_entity)
        if not result.modified_count:
            raise MongoRepositoryError()

        db_result = self._get_database_entity(entity.id)
        if not db_result:
            raise NotFoundError()

        return self._to_domain_entity(db_result)

    def delete(self, entity: T, /) -> None:
        self.collection.delete_one({"_id": ObjectId(entity.id)})

    def _get_database_entity(self, entity_id: str, /) -> MongoDocument | None:
        pipeline = [
            {"$match": {"_id": ObjectId(entity_id)}},
            *self._aggregation_pipeline(),
        ]
        return next(self.collection.aggregate(pipeline), None)

    def _to_domain_entity(self, document: MongoDocument, /) -> T:
        document["id"] = str(document.pop("_id"))
        return self.domain_model.model_validate(document)

    @staticmethod
    def _to_database_entity(entity: T, /) -> MongoDocument:
        document = entity.model_dump(exclude={"id"})
        document["_id"] = entity.id
        return document

    def _search_pipeline(self, search: str, /) -> list[MongoDocument]:
        conditions = [
            {field: {"$regex": search, "$options": "i"}}
            for field in self.searchable_fields
        ]
        return [{"$match": {"$or": conditions}}]

    @staticmethod
    def _aggregation_pipeline() -> list[MongoDocument]:
        return []
