from typing import Any, Self

from bson import ObjectId
from cleanstack.infrastructure.mongodb.types import MongoDocument

from app.domain.entities import Pagination, SortEntity, SortOrder
from app.domain.filters import FilterEntity, FilterOperator


class PipelineBuilder:
    def __init__(self) -> None:
        self._order_map = {SortOrder.ASC: 1, SortOrder.DESC: -1}
        self._base_stages: list[MongoDocument] = []
        self._sort_stage: list[MongoDocument] = []
        self._pagination_stage: list[MongoDocument] = []

    def add_search(
        self,
        search: str | None,
        searchable_fields: tuple[str, ...],
    ) -> Self:
        if not search:
            return self

        or_conditions = [
            {field: {"$regex": search.strip(), "$options": "i"}}
            for field in searchable_fields
        ]
        search_stage = {"$match": {"$or": or_conditions}}

        self._base_stages.append(search_stage)
        return self

    def add_filters(self, filters: list[FilterEntity] | None) -> Self:
        if not filters:
            return self

        match_query = {}

        for filter_ in filters:
            field, value = self._format_value(filter_.field, filter_.value)

            match filter_.operator:
                case FilterOperator.EQ:
                    match_query[field] = value
                case FilterOperator.IN:
                    match_query[field] = {"$in": value}
        match_stage = {"$match": match_query}

        self._base_stages.append(match_stage)
        return self

    def add_lookups(self, lookups: list[MongoDocument]) -> Self:
        self._base_stages.extend(lookups)
        return self

    def add_sort(self, sort: list[SortEntity] | None) -> Self:
        if not sort:
            return self

        sort_query = {entity.field: self._order_map[entity.order] for entity in sort}
        sort_stage = {"$sort": sort_query}

        self._sort_stage = [sort_stage]
        return self

    def add_pagination(self, pagination: Pagination) -> Self:
        self._pagination_stage = [
            {"$skip": pagination.skip},
            {"$limit": pagination.limit},
        ]
        return self

    @property
    def count(self) -> list[MongoDocument]:
        return [*self._base_stages, {"$count": "total"}]

    @property
    def data(self) -> list[MongoDocument]:
        return self._base_stages + self._sort_stage + self._pagination_stage

    @staticmethod
    def _format_value(field: str, value: Any) -> tuple[str, Any]:
        if field == "id":
            if isinstance(value, list):
                return "_id", [ObjectId(v) for v in value]
            return "_id", ObjectId(value)
        return field, value
