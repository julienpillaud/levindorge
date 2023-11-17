from typing import Any, Mapping

from bson import ObjectId
from pymongo import ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import (
    DeleteResult,
    InsertOneResult,
    UpdateResult,
    InsertManyResult,
)

from application.entities.article import (
    Article,
    ArticleType,
    CreateOrUpdateArticle,
    ExtendedArticle,
)
from application.entities.inventory import (
    CreateInventoryRecord,
    InventoryRecord,
    CreateInventory,
    Inventory,
    UpdateInventory,
)
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
        return [
            ArticleType.model_validate(article_type) for article_type in article_types
        ]

    def get_ratio_category(self, list_category: str) -> str:
        """Get the ratio category for a given list category."""
        article_types = self.database.types.find({"list_category": list_category})
        return article_types[0]["ratio_category"]

    def get_article_type(self, type_name: str) -> ArticleType:
        """Get an ArticleType for a given name."""
        article_type = self.database.types.find_one({"name": type_name})
        return ArticleType.model_validate(article_type)

    def get_article_types_by_list(self, list_category: str) -> list[ArticleType]:
        """Get a list of ArticleType filtered by the specified list category."""
        article_types = self.database.types.find({"list_category": list_category})
        return [
            ArticleType.model_validate(article_type) for article_type in article_types
        ]

    def get_article_types_by_lists(
        self, lists_category: list[str]
    ) -> list[ArticleType]:
        article_types = self.database.types.find(
            {"list_category": {"$in": lists_category}}
        )
        return [
            ArticleType.model_validate(article_type) for article_type in article_types
        ]

    # --------------------------------------------------------------------------
    # catalog
    def get_articles(
        self, filter: dict[str, Any] | None = None, to_validate: bool = False
    ) -> list[Article]:
        sort_key = "type"
        if filter is None:
            filter = {}
        if to_validate:
            sort_key = "created_at"
            filter.update({"validated": False})

        articles = self.database.catalog.find(filter).sort(sort_key)
        return [Article.model_validate(article) for article in articles]

    def get_extended_articles(self) -> list[ExtendedArticle]:
        articles = self.database.catalog.aggregate(
            [
                {
                    "$lookup": {
                        "from": "types",
                        "localField": "type",
                        "foreignField": "name",
                        "as": "article_type",
                    }
                },
                {"$unwind": "$article_type"},
            ]
        )
        return [ExtendedArticle.model_validate(article) for article in articles]

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
        return [Article.model_validate(article) for article in articles]

    def get_article_by_id(self, article_id: str) -> Article:
        """Retrieve an article by its unique id."""
        article = self.database.catalog.find_one({"_id": ObjectId(article_id)})
        return Article.model_validate(article)

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
        return [Shop.model_validate(shop) for shop in self.database.shops.find()]

    def get_user_shops(self, user_shops: list[str]) -> list[Shop]:
        user_shops_db = self.database.shops.find(
            {"username": {"$in": user_shops}}
        ).sort("name")
        return [Shop.model_validate(shop) for shop in user_shops_db]

    def get_shop_by_username(self, username: str) -> Shop:
        """Retrieve a shop by its username."""
        shop = self.database.shops.find_one({"username": username})
        return Shop.model_validate(shop)

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
        return [Item.model_validate(item) for item in collection.find().sort("name")]

    def get_item_by_id(self, category: str, item_id: str) -> Item:
        collection = self.get_collection(category)
        item = collection.find_one({"_id": ObjectId(item_id)})
        return Item.model_validate(item)

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
    def get_inventories(self) -> list[Inventory]:
        inventories = self.database.inventory.find()
        return [Inventory.model_validate(inventory) for inventory in inventories]

    def get_inventory(self, inventory_id: str) -> Inventory:
        inventory = self.database.inventory.find_one({"_id": ObjectId(inventory_id)})
        return Inventory.model_validate(inventory)

    def create_inventory(self, inventory: CreateInventory) -> InsertOneResult:
        return self.database.inventory.insert_one(inventory.model_dump())

    def update_inventory(
        self, inventory_id: str, inventory: UpdateInventory
    ) -> UpdateResult:
        return self.database.inventory.update_one(
            {"_id": ObjectId(inventory_id)},
            {
                "$set": {
                    "inventory": inventory.inventory.model_dump(),
                    "sale_value": inventory.sale_value,
                    "deposit_value": inventory.deposit_value,
                }
            },
        )

    def delete_inventory(self, inventory_id: str) -> DeleteResult:
        return self.database.inventory.delete_one({"_id": ObjectId(inventory_id)})

    def get_inventory_records(self, inventory_id: str) -> list[InventoryRecord]:
        inventory_records = self.database.inventory_records.find(
            {"inventory_id": inventory_id}
        ).sort(
            [
                ("article_type", ASCENDING),
                ("article_name.name1", ASCENDING),
                ("article_name.name2", ASCENDING),
            ]
        )
        return [
            InventoryRecord.model_validate(inventory_record)
            for inventory_record in inventory_records
        ]

    def save_inventory_records(
        self,
        inventory_records: list[CreateInventoryRecord],
    ) -> InsertManyResult:
        return self.database.inventory_records.insert_many(
            [inventory_record.model_dump() for inventory_record in inventory_records]
        )

    def delete_inventory_records(self, inventory_id: str) -> DeleteResult:
        return self.database.inventory_records.delete_many(
            {"inventory_id": inventory_id}
        )
