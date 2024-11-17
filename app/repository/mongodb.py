from collections.abc import Mapping
from typing import Any

from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import (
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)

from app.entities.article import (
    Article,
    ArticleType,
    CreateOrUpdateArticle,
    ExtendedArticle,
)
from app.entities.deposit import Deposit, RequestDeposit
from app.entities.inventory import (
    CreateInventory,
    CreateInventoryRecord,
    Inventory,
    InventoryRecord,
    UpdateInventory,
)
from app.entities.item import Item, RequestItem
from app.entities.shop import Shop
from app.entities.volume import RequestVolume, Volume
from app.interfaces.repository import IRepository


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

        articles = self.database.articles.find(filter).sort(sort_key)
        return [Article.model_validate(article) for article in articles]

    def get_extended_articles(self) -> list[ExtendedArticle]:
        articles = self.database.articles.aggregate(
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
        articles = self.database.articles.find(
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
        article = self.database.articles.find_one({"_id": ObjectId(article_id)})
        return Article.model_validate(article)

    def create_article(self, article: CreateOrUpdateArticle) -> InsertOneResult:
        """Create a new article."""
        return self.database.articles.insert_one(article.model_dump())

    def update_article(
        self, article_id: str, article: CreateOrUpdateArticle
    ) -> UpdateResult:
        """Update an existing article."""
        return self.database.articles.replace_one(
            {"_id": ObjectId(article_id)}, article.model_dump()
        )

    def update_article_stock_quantity(
        self, article_id: str, stock_quantity: int, shop: Shop
    ) -> UpdateResult:
        return self.database.articles.update_one(
            {"_id": ObjectId(article_id)},
            {"$set": {f"shops.{shop.username}.stock_quantity": stock_quantity}},
        )

    def delete_article(self, article_id: str) -> DeleteResult:
        """Delete an article."""
        return self.database.articles.delete_one({"_id": ObjectId(article_id)})

    def validate_article(self, article_id: str) -> UpdateResult:
        """Set the 'validated' field to true."""
        return self.database.articles.update_one(
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
    def get_items_dict(self, volume_category: str) -> dict[str, Any]:
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

    def delete_item(self, category: str, item_id: str) -> DeleteResult | None:
        collection = self.get_collection(category)
        item = self.get_item_by_id(category=category, item_id=item_id)
        if self.item_is_used(category=category, item=item):
            return None
        return collection.delete_one({"_id": ObjectId(item_id)})

    def item_is_used(self, category: str, item: Item) -> bool:
        if category == "distributors":
            return bool(self.database.articles.find_one({"distributor": item.name}))
        elif category in {"breweries", "distilleries"}:
            return bool(self.database.articles.find_one({"name.name1": item.name}))
        elif category in {"countries", "regions"}:
            return bool(self.database.articles.find_one({"region": item.name}))
        else:
            return False

    def get_volumes_by_category(self, volume_category: str) -> list[Volume]:
        return [
            Volume.model_validate(volume)
            for volume in self.database.volumes.find(
                {"category": volume_category}
            ).sort("value")
        ]

    def get_volumes(self) -> list[Volume]:
        return [
            Volume.model_validate(volume)
            for volume in self.database.volumes.find().sort(
                [("category", ASCENDING), ("value", ASCENDING)]
            )
        ]

    def create_volume(self, volume: RequestVolume) -> InsertOneResult:
        return self.database.volumes.insert_one(volume.model_dump())

    def get_volume_by_id(self, volume_id: str) -> Volume:
        volume = self.database.volumes.find_one({"_id": ObjectId(volume_id)})
        return Volume.model_validate(volume)

    def delete_volume(self, volume_id: str) -> DeleteResult | None:
        volume = self.get_volume_by_id(volume_id=volume_id)
        if self.volume_is_used(volume=volume):
            return None
        return self.database.volumes.delete_one({"_id": ObjectId(volume_id)})

    def volume_is_used(self, volume) -> bool:
        types = self.database.types.find({"volume_category": volume.category})
        return bool(
            self.database.articles.find_one(
                {"volume": volume.value, "type": {"$in": [x["name"] for x in types]}}
            )
        )

    def get_deposits(self) -> list[Deposit]:
        return [
            Deposit.model_validate(item)
            for item in self.database.deposits.find().sort(
                [
                    ("category", ASCENDING),
                    ("deposit_type", DESCENDING),
                    ("value", ASCENDING),
                ]
            )
        ]

    def get_deposit_by_id(self, deposit_id: str) -> Deposit:
        deposit = self.database.deposits.find_one({"_id": ObjectId(deposit_id)})
        return Deposit.model_validate(deposit)

    def create_deposit(self, deposit: RequestDeposit) -> InsertOneResult:
        return self.database.deposits.insert_one(deposit.model_dump())

    def delete_deposit(self, deposit_id: str) -> DeleteResult | None:
        deposit = self.get_deposit_by_id(deposit_id=deposit_id)
        if self.deposit_is_used(deposit=deposit):
            return None
        return self.database.deposits.delete_one({"_id": ObjectId(deposit_id)})

    def deposit_is_used(self, deposit: Deposit):
        deposit_type_mapping = {"Unitaire": "unit", "Caisse": "case"}
        deposit_key = deposit_type_mapping[deposit.deposit_type]
        return bool(
            self.database.articles.find_one({f"deposit.{deposit_key}": deposit.value})
        )

    # --------------------------------------------------------------------------
    # inventory
    def get_inventories(self) -> list[Inventory]:
        inventories = self.database.inventories.find()
        return [Inventory.model_validate(inventory) for inventory in inventories]

    def get_inventory(self, inventory_id: str) -> Inventory:
        inventory = self.database.inventories.find_one({"_id": ObjectId(inventory_id)})
        return Inventory.model_validate(inventory)

    def create_inventory(self, inventory: CreateInventory) -> InsertOneResult:
        return self.database.inventories.insert_one(inventory.model_dump())

    def update_inventory(
        self, inventory_id: str, inventory: UpdateInventory
    ) -> UpdateResult:
        return self.database.inventories.update_one(
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
        return self.database.inventories.delete_one({"_id": ObjectId(inventory_id)})

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
