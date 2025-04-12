from copy import deepcopy
from typing import Any, TypeVar

from pymongo import ASCENDING
from pymongo.database import Database

from app.domain.articles.entities import Article, TypeInfos
from app.domain.entities import DomainModel
from app.domain.repository import RepositoryProtocol
from app.domain.users.entities import User
from app.infrastructure.utils import to_user_domain

T = TypeVar("T", bound=DomainModel)


class MongoRepository(RepositoryProtocol):
    def __init__(self, database: Database[dict[str, Any]]):
        self.database = database

    @staticmethod
    def _to_domain(entity_type: type[T], db_entity: dict[str, Any]) -> T:
        data = deepcopy(db_entity)
        entity_id = str(data.pop("_id"))
        return entity_type(id=entity_id, **data)

    def get_user_by_email(self, email: str) -> User | None:
        user = self.database.users.find_one({"email": email})
        if not user:
            return None

        shops = list(self.database.shops.find({"username": {"$in": user["shops"]}}))
        return to_user_domain(user=user, shops=shops)

    def get_articles_by_list_category(self, list_category: str) -> list[Article]:
        article_types = self._get_article_types_by_list_category(
            list_category=list_category
        )
        article_types_names = [article_type.name for article_type in article_types]
        pipeline = [
            {"$match": {"type": {"$in": article_types_names}}},
            {
                "$lookup": {
                    "from": "types",
                    "localField": "type",
                    "foreignField": "name",
                    "as": "type_infos",
                }
            },
            {"$unwind": "$type_infos"},
            {
                "$sort": {
                    "type": ASCENDING,
                    "region": ASCENDING,
                    "name.name1": ASCENDING,
                    "name.name2": ASCENDING,
                }
            },
        ]
        articles = self.database.articles.aggregate(pipeline)

        return [
            self._to_domain(entity_type=Article, db_entity=article)
            for article in articles
        ]

    def _get_article_types_by_list_category(
        self, list_category: str
    ) -> list[TypeInfos]:
        article_types = self.database.types.find({"list_category": list_category})
        return [
            TypeInfos.model_validate(article_type) for article_type in article_types
        ]
