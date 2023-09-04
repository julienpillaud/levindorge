import os
from collections import OrderedDict

from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo import ASCENDING, MongoClient

load_dotenv()
mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri, document_class=OrderedDict)

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


def get_shops():
    """Get all shops"""
    return shops.find().sort("id")


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# USERS
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def get_user_by_email(email):
    """Retourne le DICT utilisateur à partir de son email"""
    return users.find_one({"email": email})


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# SHOPS
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def get_shop_usernames():
    return [x["username"] for x in shops.find({})]


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


def get_tactill_api_key(username):
    return shops.find_one({"username": username})["tactill_api_key"]


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# CATALOG
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def get_articles():
    """Retourne le CURSOR de tous les articles"""
    return catalog.find({}).sort([("type", ASCENDING)])


def get_articles_by_list(list_category):
    """Retourne le CURSOR des articles triés correspondant au list_category"""
    type_list = get_types_by_list([list_category])
    return catalog.find({"type": {"$in": type_list}}).sort(
        [
            ("type", ASCENDING),
            ("region", ASCENDING),
            ("name.name1", ASCENDING),
            ("name.name2", ASCENDING),
        ]
    )


def get_article_by_id(article_id):
    """Retourne le DICT article par son ID"""
    return catalog.find_one({"_id": ObjectId(article_id)})


def get_articles_by_filter(filter):
    return catalog.find(filter)


def create_article(article):
    """Créer un article à partie du DICT"""
    return catalog.insert_one(article)


def update_article(article_id, article):
    """Remplace l'article"""
    return catalog.replace_one({"_id": ObjectId(article_id)}, article)


def delete_article(article_id):
    """Supprime l'article"""
    return catalog.delete_one({"_id": ObjectId(article_id)})


def get_articles_to_validate():
    """Retourne le CURSOR des articles qui ne sont pas validés"""
    return catalog.find({"validated": False})


def validate_article(article_id):
    """Valide l'article"""
    return catalog.update_one(
        {"_id": ObjectId(article_id)}, {"$set": {"validated": True}}, upsert=False
    )


def update_stock_quantity(article_id, shop, stock_quantity):
    field = f"shops.{shop}.stock_quantity"
    return catalog.update_one(
        {"_id": ObjectId(article_id)}, {"$set": {field: stock_quantity}}
    )


def update_barcode(article_id, barcode):
    return catalog.update_one(
        {"_id": ObjectId(article_id)}, {"$set": {"barcode": barcode}}
    )


def update_article_shops(article_id, shop, article_shops):
    field = f"shops.{shop}"
    return catalog.update_one(
        {"_id": ObjectId(article_id)}, {"$set": {field: article_shops}}
    )


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# TYPES
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def get_types_dict():
    return {
        x["name"]: {
            "list_category": x["list_category"],
            "ratio_category": x["ratio_category"],
        }
        for x in types.find({})
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


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# DROPDOWN
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
    volumes_ = types_.get("volumes", [])
    return [str(x).rstrip("0").rstrip(".") for x in volumes_]


# -----------------------------------------------------------------------------------------------------------------------
def get_dropdown_by_category(category):
    dropdown_collection = DROPDOWN_DICT[category]["collection"]
    return dropdown_collection.find({}).sort([("name", ASCENDING)])


# -----------------------------------------------------------------------------------------------------------------------
def create_dropdown(dropdown_category, dropdown):
    dropdown_collection = DROPDOWN_DICT[dropdown_category]["collection"]
    return dropdown_collection.insert_one(dropdown)


def delete_dropdown(dropdown_category, dropdown_id):
    dropdown_collection = DROPDOWN_DICT[dropdown_category]["collection"]
    return dropdown_collection.delete_one({"_id": ObjectId(dropdown_id)})
