from typing import Any

from bson import ObjectId

from app.domain.filters import FilterEntity, FilterOperator
from app.infrastructure.repository.types import MongoDocument


class MongoQueryBuilder:
    @staticmethod
    def build_search_stage(
        search_string: str,
        searchable_fields: tuple[str, ...],
    ) -> MongoDocument:
        or_conditions = [
            {field: {"$regex": search_string.strip(), "$options": "i"}}
            for field in searchable_fields
        ]
        return {"$match": {"$or": or_conditions}}

    @staticmethod
    def build_filters_stage(filters: list[FilterEntity]) -> MongoDocument:
        match_query = {}

        for filter_ in filters:
            field, value = MongoQueryBuilder._format_value(filter_.field, filter_.value)

            match filter_.operator:
                case FilterOperator.EQ:
                    match_query[field] = value
                case FilterOperator.IN:
                    match_query[field] = {"$in": value}

        return {"$match": match_query}

    @staticmethod
    def _format_value(field: str, value: Any) -> tuple[str, Any]:
        if field == "id":
            if isinstance(value, list):
                return "_id", [ObjectId(v) for v in value]
            return "_id", ObjectId(value)
        return field, value
