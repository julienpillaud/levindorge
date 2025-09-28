from typing import Any

from bson import ObjectId
from cleanstack.exceptions import NotFoundError
from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo import ASCENDING, DESCENDING
from pymongo.collection import Collection
from pymongo.database import Database

from app.domain.articles.entities import Article
from app.domain.commons.entities import ArticleType, Deposit, DisplayGroup, Item, Volume
from app.domain.entities import EntityId
from app.domain.protocols.repository import RepositoryProtocol
from app.domain.shops.entities import Shop
from app.domain.users.entities import User


class MongoRepositoryError(Exception):
    pass


class MongoRepository(RepositoryProtocol):
    def __init__(self, database: Database[MongoDocument]):
        self.database = database

    def _get_collection(self, name: str) -> Collection[MongoDocument]:
        return self.database.get_collection(name)

    # Collection 'users'
    def get_user_by_email(self, email: str) -> User | None:
        user = self.database.users.find_one({"email": email})
        if not user:
            return None

        shops = list(self.database.shops.find({"username": {"$in": user["shops"]}}))

        return User(
            id=str(user["_id"]),
            name=user["name"],
            username=user["username"],
            email=user["email"],
            hashed_password=user["password"],
            shops=[
                Shop(
                    id=str(shop["_id"]),
                    name=shop["name"],
                    username=shop["username"],
                    tactill_api_key=shop["tactill_api_key"],
                    margins=shop["margins"],
                )
                for shop in shops
            ],
            role=user["role"],
        )

    # Collection shops
    def get_shops(self) -> list[Shop]:
        return [Shop(**shop) for shop in self.database["shops"].find()]

    # Collection 'types'
    def get_article_types(
        self,
        name: str | None = None,
        display_group: DisplayGroup | None = None,
    ) -> list[ArticleType]:
        query_filter = {}
        if name is not None:
            query_filter["name"] = name
        if display_group is not None:
            query_filter["list_category"] = display_group

        article_types = self.database["types"].find(query_filter)
        return [ArticleType(**article_type) for article_type in article_types]

    def get_article_type_by_name(self, name: str) -> ArticleType:
        article_type = self.database["types"].find_one({"name": name})
        if not article_type:
            raise NotFoundError()

        return ArticleType(**article_type)

    def get_article_types_by_list(
        self,
        display_group: DisplayGroup,
    ) -> list[ArticleType]:
        article_types = self.database["types"].find({"list_category": display_group})
        return [ArticleType(**article_type) for article_type in article_types]

    # Collection 'articles'
    def get_all_articles(self) -> list[Article]:
        articles = self.database["articles"].find().sort("type")
        return [Article.model_validate(article) for article in articles]

    def get_articles_by_display_group(
        self, display_group: DisplayGroup
    ) -> list[Article]:
        article_types = self.get_article_types_by_list(display_group)
        article_types_names = [x.name for x in article_types]
        articles = (
            self.database["articles"]
            .find({"type": {"$in": article_types_names}})
            .sort(
                [
                    ("type", ASCENDING),
                    ("region", ASCENDING),
                    ("name.name1", ASCENDING),
                    ("name.name2", ASCENDING),
                ]
            )
        )
        return [Article(**article) for article in articles]

    def get_article(self, article_id: EntityId) -> Article | None:
        article = self.database["articles"].find_one({"_id": ObjectId(article_id)})
        return Article(**article) if article else None

    def create_article(self, article: Article) -> Article:
        result = self.database["articles"].insert_one(
            article.model_dump(exclude={"id"})
        )
        return self._get_article_by_id(article_id=result.inserted_id)

    def update_article(self, article: Article) -> Article:
        result = self.database["articles"].replace_one(
            {"_id": ObjectId(article.id)},
            article.model_dump(exclude={"id"}),
        )
        if not result.modified_count:
            raise MongoRepositoryError()
        return self._get_article_by_id(article_id=article.id)

    def delete_article(self, article: Article) -> None:
        self.database["articles"].delete_one({"_id": ObjectId(article.id)})

    def _get_article_by_id(self, article_id: str) -> Article:
        article_db = self.database["articles"].find_one({"_id": ObjectId(article_id)})
        if not article_db:
            raise NotFoundError()

        return Article(**article_db)

    # Items
    def get_items_dict(self, volume_category: str | None) -> dict[str, Any]:
        return {
            "country_list": self.get_items("countries"),
            "region_list": self.get_items("regions"),
            "brewery_list": self.get_items("breweries"),
            "distillery_list": self.get_items("distilleries"),
            "distributor_list": self.get_items("distributors"),
            "volumes": self.get_volumes_by_category(volume_category),
            "deposits": self.get_deposits(),
        }

    def get_items(self, category: str) -> list[Item]:
        collection = self._get_collection(category)
        return [Item(**item) for item in collection.find().sort("name")]

    def get_volumes_by_category(self, volume_category: str | None) -> list[Volume]:
        return [
            Volume(**volume)
            for volume in self.database["volumes"]
            .find({"category": volume_category})
            .sort("value")
        ]

    def get_deposits(self) -> list[Deposit]:
        return [
            Deposit(**item)
            for item in self.database.deposits.find().sort(
                [
                    ("category", ASCENDING),
                    ("deposit_type", DESCENDING),
                    ("value", ASCENDING),
                ]
            )
        ]
