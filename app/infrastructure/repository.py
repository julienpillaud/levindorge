from copy import deepcopy
from typing import Any, TypeVar

from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from pymongo.collection import Collection
from pymongo.database import Database

from app.domain.articles.entities import Article, ArticleToDb, TypeInfos
from app.domain.entities import DomainModel
from app.domain.exceptions import EntityNotFoundError
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
        articles = self._get_articles({"type": {"$in": article_types_names}})

        return [
            self._to_domain(entity_type=Article, db_entity=article)
            for article in articles
        ]

    def get_article_by_id(self, article_id: str) -> Article:
        articles = self._get_articles({"_id": ObjectId(article_id)}, find_one=True)
        if not articles:
            raise EntityNotFoundError(f"Article '{article_id}' not found.")

        article = articles[0]
        return self._to_domain(entity_type=Article, db_entity=article)

    def create_article(self, article: ArticleToDb) -> Article:
        result = self.database.articles.insert_one(article.model_dump())
        return self.get_article_by_id(article_id=result.inserted_id)

    def update_article(self, article: Article) -> Article:
        result = self.database.articles.replace_one(
            {"_id": article.id},
            article.model_dump(exclude={"id", "type_infos"}),
        )
        return self.get_article_by_id(article_id=result.upserted_id)

    def delete_article(self, article: Article) -> None:
        self.database.articles.delete_one({"_id": ObjectId(article.id)})

    def get_type_infos_by_list_category(self, list_category: str):
        type_infos = self.database.types.find({"list_category": list_category})
        return [TypeInfos.model_validate(type_info) for type_info in type_infos]

    def get_template_context(self, volume_category: str | None) -> dict[str, Any]:
        return {
            "countries": self._get_context_entities("countries"),
            "regions": self._get_context_entities("regions"),
            "breweries": self._get_context_entities("breweries"),
            "distilleries": self._get_context_entities("distilleries"),
            "distributors": self._get_context_entities("distributors"),
            "volumes": self._get_volumes_by_category(category=volume_category)
            if volume_category
            else {},
            "deposits": self._get_deposits(),
        }

    def _get_collection(self, name: str) -> Collection[dict[str, Any]]:
        return self.database.get_collection(name)

    def _get_context_entities(self, collection_name: str) -> list[dict[str, Any]]:
        collection = self._get_collection(name=collection_name)
        return list(collection.find().sort("name"))

    def _get_volumes_by_category(self, category: str) -> list[dict[str, Any]]:
        return list(self.database.volumes.find({"category": category}).sort("value"))

    def _get_deposits(self) -> list[dict[str, Any]]:
        return list(
            self.database.deposits.find().sort(
                [
                    ("category", ASCENDING),
                    ("deposit_type", DESCENDING),
                    ("value", ASCENDING),
                ]
            )
        )

    def _assert_entity_exists(self, collection_name: str, entity_id: ObjectId) -> None:
        collection = self._get_collection(name=collection_name)
        entity = collection.find_one({"_id": entity_id})
        if not entity:
            raise EntityNotFoundError(f"Entity '{entity_id}' not found.")

    def _get_articles(
        self,
        match: dict[str, Any],
        /,
        *,
        find_one: bool | None = None,
    ) -> list[dict[str, Any]]:
        pipeline = [
            {"$match": match},
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
        if find_one:
            pipeline.append({"$limit": 1})

        return list(self.database.articles.aggregate(pipeline))

    def _get_article_types_by_list_category(
        self, list_category: str
    ) -> list[TypeInfos]:
        article_types = self.database.types.find({"list_category": list_category})
        return [
            TypeInfos.model_validate(article_type) for article_type in article_types
        ]
