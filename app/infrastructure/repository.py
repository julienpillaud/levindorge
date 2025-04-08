from copy import deepcopy
from typing import Any, TypeVar

from pymongo import ASCENDING
from pymongo.database import Database

from app.domain.articles.entities import Article, ArticleType
from app.domain.entities import DomainModel
from app.domain.repository import RepositoryProtocol
from app.domain.users.entities import User
from app.infrastructure.utils import to_user_domain

T = TypeVar("T", bound=DomainModel)


class MongoRepository(RepositoryProtocol):
    def __init__(self, database: Database[dict[str, Any]]):
        self.database = database

    @staticmethod
    def _to_domain(db_entity: dict[str, Any], entity_type: type[T]) -> T:
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
        request_filter = {
            "type": {"$in": [article_type.name for article_type in article_types]}
        }
        request_sort = [
            (field, ASCENDING)
            for field in ("type", "region", "name.name1", "name.name2")
        ]
        articles = self.database.articles.find(request_filter).sort(request_sort)
        return [
            self._to_domain(db_entity=article, entity_type=Article)
            for article in articles
        ]

    def _get_article_types_by_list_category(
        self, list_category: str
    ) -> list[ArticleType]:
        article_types = self.database.types.find({"list_category": list_category})
        return [
            ArticleType.model_validate(article_type) for article_type in article_types
        ]
