import os
from typing import Any

from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo import ASCENDING, MongoClient
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from application.entities.article import (
    Article,
    ArticleType,
    CreateOrUpdateArticle,
    InventoryArticle,
)
from application.entities.inventory import CreateOrUpdateInventory
from application.entities.item import Item, RequestItem
from application.entities.shop import Shop

load_dotenv()
mongo_uri = os.environ.get("MONGO_URI")
client: MongoClient = MongoClient(mongo_uri)

db = client.dashboard
catalog = db.catalog
breweries = db.breweries
countries = db.countries
distilleries = db.distilleries
distributors = db.distributors
regions = db.regions
volumes = db.volumes
types = db.types
users = db.users
shops = db.shops

DROPDOWN_DICT = {
    "breweries": {"name": "Brasserie", "collection": breweries},
    "countries": {"name": "Pays", "collection": countries},
    "distilleries": {"name": "Distillerie", "collection": distilleries},
    "distributors": {"name": "Fournisseur", "collection": distributors},
    "regions": {"name": "Région", "collection": regions},
    "volumes": {"name": "Volume", "collection": volumes},
}


def get_collection(name: str):
    return db.get_collection(name)


# ------------------------------------------------------------------------------
# users
def get_user_by_email(email: str):
    """Retrieve a user by its email address."""
    return users.find_one({"email": email}, {"_id": 0})


# ------------------------------------------------------------------------------
# types
def get_ratio_category(list_category: str) -> str:
    """Get the ratio category for a given list category."""
    article_types = types.find({"list_category": list_category})
    return article_types[0]["ratio_category"]


def get_article_type(type_name: str) -> ArticleType:
    """Get an ArticleType for a given name."""
    article_type = types.find_one({"name": type_name})
    return ArticleType(**article_type)


def get_article_types_by_list(list_category: str) -> list[ArticleType]:
    """Get a list of ArticleType filtered by the specified list category."""
    article_types = types.find({"list_category": list_category})
    return [ArticleType(**x) for x in article_types]


def get_article_types_by_lists(lists_category: list[str]) -> list[ArticleType]:
    article_types = types.find({"list_category": {"$in": lists_category}})
    return [ArticleType(**x) for x in article_types]


# ------------------------------------------------------------------------------
# catalog
def get_articles(
    filter: dict[str, Any] | None = None, to_validate: bool = False
) -> list[Article]:
    if filter is None:
        filter = {}
    if to_validate:
        filter.update({"validated": False})

    articles = catalog.find(filter).sort([("type", ASCENDING)])
    return [Article(**x) for x in articles]


def get_articles_by_list(list_category: str) -> list[Article]:
    """Retrieve a list of articles filtered by list category."""
    article_types = get_article_types_by_list(list_category)
    article_types_names = [x.name for x in article_types]
    articles = catalog.find({"type": {"$in": article_types_names}}).sort(
        [
            ("type", ASCENDING),
            ("region", ASCENDING),
            ("name.name1", ASCENDING),
            ("name.name2", ASCENDING),
        ]
    )
    return [Article(**x) for x in articles]


def get_article_by_id(article_id: str) -> Article:
    """Retrieve an article by its unique id."""
    article = catalog.find_one({"_id": ObjectId(article_id)})
    return Article(**article)


def create_article(article: CreateOrUpdateArticle) -> InsertOneResult:
    """Create a new article."""
    return catalog.insert_one(article.model_dump())


def update_article(article_id: str, article: CreateOrUpdateArticle) -> UpdateResult:
    """Update an existing article."""
    return catalog.replace_one({"_id": ObjectId(article_id)}, article.model_dump())


def delete_article(article_id: str) -> DeleteResult:
    """Delete an article."""
    return catalog.delete_one({"_id": ObjectId(article_id)})


def validate_article(article_id):
    """Set the 'validated' field to true."""
    return catalog.update_one(
        {"_id": ObjectId(article_id)}, {"$set": {"validated": True}}, upsert=False
    )


# ------------------------------------------------------------------------------
# shops
def get_shops() -> list[Shop]:
    """Get the list of all shops"""
    return [Shop(**shop) for shop in shops.find()]


def get_shop_by_username(username: str) -> Shop:
    """Retrieve a shop by its username."""
    shop = shops.find_one({"username": username})
    return Shop(**shop)


# ------------------------------------------------------------------------------
def get_items(category: str) -> list[Item]:
    collection = get_collection(category)
    return [Item(**item) for item in collection.find().sort("name")]


def create_item(category: str, item: RequestItem) -> InsertOneResult:
    collection = get_collection(category)
    item = item.model_dump()
    if category != "countries":
        item.pop("demonym")
    return collection.insert_one(item)


def delete_item(category: str, item_id: str) -> DeleteResult:
    collection = get_collection(category)
    return collection.delete_one({"_id": ObjectId(item_id)})


# ------------------------------------------------------------------------------
# inventory
def save_inventory_record(inventory_record: CreateOrUpdateInventory) -> InsertOneResult:
    return db.inventory.replace_one(
        {"article_id": inventory_record.article_id},
        inventory_record.model_dump(),
        upsert=True,
    )


def reset_inventory():
    db.inventory.delete_many({})


def get_articles_inventory(match):
    articles = db.catalog.aggregate(
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


def get_articles_for_inventory():
    beer1 = get_articles_inventory(
        {"type": {"$in": ["Bière", "Cidre"]}, "deposit.unit": {"$ne": 0}}
    )
    beer2 = list(
        get_articles_inventory(
            {"type": {"$in": ["Bière", "Cidre"]}, "deposit.unit": {"$eq": 0}}
        )
    )
    keg = get_articles_inventory({"type": {"$in": ["Fût", "Mini-fût"]}})
    spirit_types = get_article_types_by_lists(["rhum", "whisky", "arranged", "spirit"])
    spirit = get_articles_inventory({"type": {"$in": [x.name for x in spirit_types]}})
    wine_types = get_article_types_by_lists(
        ["wine", "fortified_wine", "sparkling_wine"]
    )
    wine = get_articles_inventory({"type": {"$in": [x.name for x in wine_types]}})
    bib = get_articles_inventory({"type": {"$in": ["BIB"]}})
    box = get_articles_inventory({"type": {"$in": ["Coffret"]}})
    misc = get_articles_inventory({"type": {"$in": ["Accessoire", "Emballage", "BSA"]}})
    food = get_articles_inventory({"type": {"$in": ["Alimentation"]}})

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


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def get_shops_margins(ratio_category=None):
    if ratio_category is None:
        return {
            x["username"]: {"name": x["name"], "margins": x["margins"]}
            for x in shops.find({})
        }
    else:
        return {
            x["username"]: {"name": x["name"], "margins": x["margins"][ratio_category]}
            for x in shops.find({})
        }


def get_types_by_list(list_categories):
    """
    Retourne la LIST des types correspondant à la LIST des list_category
    -> Affiche le type ou la liste déroulante en tête de la fiche créaation
    """
    return sorted(
        [x["name"] for x in types.find({"list_category": {"$in": list_categories}})]
    )


def get_type(input_key, input_value, output):
    """Retourne l'output correspondant au couple input_key: input_value"""
    return types.find_one({input_key: input_value})[output]


def get_demonym():
    return {x["name"]: x["demonym"] for x in countries.find({})}


def get_dropdown(list_category):
    """Retourn un DICT des LIST pour les listes déroulantes de la fiche création"""
    return {
        "country_list": get_countries(),
        "region_list": get_regions(),
        "brewery_list": get_breweries(),
        "distillery_list": get_distilleries(),
        "distributor_list": get_distributors(),
        "volume_list": get_volumes(list_category),
    }


def get_countries():
    return sorted([x["name"] for x in countries.find({})])


def get_regions():
    return sorted([x["name"] for x in regions.find({})])


def get_breweries():
    return sorted([x["name"] for x in breweries.find({})])


def get_distilleries():
    return sorted([x["name"] for x in distilleries.find({})])


def get_distributors():
    return sorted([x["name"] for x in distributors.find({})])


def get_volumes(list_category):
    types_ = types.find_one({"list_category": list_category})
    return types_.get("volumes", [])
