from typing import Any, Mapping

from bson import ObjectId
from pymongo import ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from application.entities.article import (
    Article,
    ArticleType,
    CreateOrUpdateArticle,
    InventoryArticle,
)
from application.entities.inventory import CreateOrUpdateInventory, Inventory
from application.entities.item import Item, RequestItem
from application.entities.shop import Shop
from application.interfaces.repository import IRepository


class MongoRepository(IRepository):
    def __init__(self, database: Database[Mapping[str, Any]]) -> None:
        self.database = database

    def get_collection(self, name: str) -> Collection[Mapping[str, Any]]:
        return self.database.get_collection(name)

    # --------------------------------------------------------------------------
    # users
    def get_user_by_email(self, email: str) -> Mapping[str, Any] | None:
        """Retrieve a user by its email address."""
        return self.database.users.find_one({"email": email}, {"_id": 0})

    # --------------------------------------------------------------------------
    # types
    def get_types(self) -> list[ArticleType]:
        article_types = self.database.types.find()
        return [ArticleType(**x) for x in article_types]

    def get_ratio_category(self, list_category: str) -> str:
        """Get the ratio category for a given list category."""
        article_types = self.database.types.find({"list_category": list_category})
        return article_types[0]["ratio_category"]

    def get_article_type(self, type_name: str) -> ArticleType:
        """Get an ArticleType for a given name."""
        article_type = self.database.types.find_one({"name": type_name})
        return ArticleType(**article_type)

    def get_article_types_by_list(self, list_category: str) -> list[ArticleType]:
        """Get a list of ArticleType filtered by the specified list category."""
        article_types = self.database.types.find({"list_category": list_category})
        return [ArticleType(**x) for x in article_types]

    def get_article_types_by_lists(
        self, lists_category: list[str]
    ) -> list[ArticleType]:
        article_types = self.database.types.find(
            {"list_category": {"$in": lists_category}}
        )
        return [ArticleType(**x) for x in article_types]

    # --------------------------------------------------------------------------
    # catalog
    def get_articles(
        self, filter: dict[str, Any] | None = None, to_validate: bool = False
    ) -> list[Article]:
        if filter is None:
            filter = {}
        if to_validate:
            filter.update({"validated": False})

        articles = self.database.catalog.find(filter).sort([("type", ASCENDING)])
        return [Article(**x) for x in articles]

    def get_articles_by_list(self, list_category: str) -> list[Article]:
        """Retrieve a list of articles filtered by list category."""
        article_types = self.get_article_types_by_list(list_category)
        article_types_names = [x.name for x in article_types]
        articles = self.database.catalog.find(
            {"type": {"$in": article_types_names}}
        ).sort(
            [
                ("type", ASCENDING),
                ("region", ASCENDING),
                ("name.name1", ASCENDING),
                ("name.name2", ASCENDING),
            ]
        )
        return [Article(**x) for x in articles]

    def get_article_by_id(self, article_id: str) -> Article:
        """Retrieve an article by its unique id."""
        article = self.database.catalog.find_one({"_id": ObjectId(article_id)})
        return Article(**article)

    def create_article(self, article: CreateOrUpdateArticle) -> InsertOneResult:
        """Create a new article."""
        return self.database.catalog.insert_one(article.model_dump())

    def update_article(
        self, article_id: str, article: CreateOrUpdateArticle
    ) -> UpdateResult:
        """Update an existing article."""
        return self.database.catalog.replace_one(
            {"_id": ObjectId(article_id)}, article.model_dump()
        )

    def delete_article(self, article_id: str) -> DeleteResult:
        """Delete an article."""
        return self.database.catalog.delete_one({"_id": ObjectId(article_id)})

    def validate_article(self, article_id: str) -> UpdateResult:
        """Set the 'validated' field to true."""
        return self.database.catalog.update_one(
            {"_id": ObjectId(article_id)}, {"$set": {"validated": True}}, upsert=False
        )

    # --------------------------------------------------------------------------
    # shops
    def get_shops(self) -> list[Shop]:
        """Get the list of all shops"""
        return [Shop(**shop) for shop in self.database.shops.find()]

    def get_user_shops(self, user_shops: list[str]) -> list[Shop]:
        user_shops_db = self.database.shops.find(
            {"username": {"$in": user_shops}}
        ).sort("name")
        return [Shop(**shop) for shop in user_shops_db]

    def get_shop_by_username(self, username: str) -> Shop:
        """Retrieve a shop by its username."""
        shop = self.database.shops.find_one({"username": username})
        return Shop(**shop)

    # ------------------------------------------------------------------------------
    # items
    def get_items_dict(self, list_category: str) -> dict[str, Any]:
        article_types = self.get_article_types_by_list(list_category)
        return {
            "country_list": self.get_items("countries"),
            "region_list": self.get_items("regions"),
            "brewery_list": self.get_items("breweries"),
            "distillery_list": self.get_items("distilleries"),
            "distributor_list": self.get_items("distributors"),
            "volume_list": article_types[0].volumes,
        }

    def get_items(self, category: str) -> list[Item]:
        collection = self.get_collection(category)
        return [Item(**item) for item in collection.find().sort("name")]

    def get_item_by_id(self, category: str, item_id: str) -> Item:
        collection = self.get_collection(category)
        item = collection.find_one({"_id": ObjectId(item_id)})
        return Item(**item)

    def create_item(self, category: str, item: RequestItem) -> InsertOneResult:
        collection = self.get_collection(category)
        item_data = item.model_dump()
        if category != "countries":
            item_data.pop("demonym")
        return collection.insert_one(item_data)

    def delete_item(self, category: str, item_id: str) -> DeleteResult:
        collection = self.get_collection(category)
        return collection.delete_one({"_id": ObjectId(item_id)})

    # --------------------------------------------------------------------------
    # inventory
    def get_inventory_record(self, article_id: str) -> Inventory:
        inventory_record = self.database.inventory.find_one({"article_id": article_id})
        return Inventory(**inventory_record)

    def save_inventory_record(
        self,
        inventory_record: CreateOrUpdateInventory,
    ) -> UpdateResult:
        return self.database.inventory.replace_one(
            {"article_id": inventory_record.article_id},
            inventory_record.model_dump(),
            upsert=True,
        )

    def reset_inventory(self) -> DeleteResult:
        return self.database.inventory.delete_many({})

    def get_articles_inventory(self, match: dict[str, Any]) -> list[InventoryArticle]:
        articles = self.database.catalog.aggregate(
            [
                {"$match": match},
                {"$addFields": {"articleId": {"$toString": "$_id"}}},
                {
                    "$lookup": {
                        "from": "inventory",
                        "localField": "articleId",
                        "foreignField": "article_id",
                        "as": "inventoryList",
                    }
                },
                {
                    "$replaceRoot": {
                        "newRoot": {
                            "$mergeObjects": [
                                "$$ROOT",
                                {"inventory": {"$arrayElemAt": ["$inventoryList", 0]}},
                            ]
                        }
                    }
                },
                {"$project": {"inventoryList": 0, "articleId": 0}},
            ]
        )
        return [InventoryArticle(**x) for x in articles]

    def get_articles_for_inventory(self) -> dict[str, list[InventoryArticle]]:
        beer1 = self.get_articles_inventory(
            {"type": {"$in": ["Bière", "Cidre"]}, "deposit.unit": {"$ne": 0}}
        )
        beer2 = list(
            self.get_articles_inventory(
                {"type": {"$in": ["Bière", "Cidre"]}, "deposit.unit": {"$eq": 0}}
            )
        )
        keg = self.get_articles_inventory({"type": {"$in": ["Fût", "Mini-fût"]}})
        spirit_types = self.get_article_types_by_lists(
            ["rhum", "whisky", "arranged", "spirit"]
        )
        spirit = self.get_articles_inventory(
            {"type": {"$in": [x.name for x in spirit_types]}}
        )
        wine_types = self.get_article_types_by_lists(
            ["wine", "fortified_wine", "sparkling_wine"]
        )
        wine = self.get_articles_inventory(
            {"type": {"$in": [x.name for x in wine_types]}}
        )
        bib = self.get_articles_inventory({"type": {"$in": ["BIB"]}})
        box = self.get_articles_inventory({"type": {"$in": ["Coffret"]}})
        misc = self.get_articles_inventory(
            {"type": {"$in": ["Accessoire", "Emballage", "BSA"]}}
        )
        food = self.get_articles_inventory({"type": {"$in": ["Alimentation"]}})

        return {
            "Bières C": beer1,
            "Bières NC": beer2,
            "Fûts": keg,
            "Spiritieux": spirit,
            "Vins": wine,
            "BIB": bib,
            "Coffrets": box,
            "Divers": misc,
            "Alimentation": food,
        }
