from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo import MongoClient

from app.core.config import Settings
from app.core.core import Context
from scripts.migration.articles import update_articles
from scripts.migration.categories import update_categories
from scripts.migration.stores import update_stores

if __name__ == "__main__":
    src_settings = Settings(mongo_database="dashboard")
    dst_settings = Settings(mongo_database="temp")
    client: MongoClient[MongoDocument] = MongoClient(src_settings.mongo_uri)
    src_database = client[src_settings.mongo_database]
    dst_database = client[dst_settings.mongo_database]
    src_context = Context(settings=src_settings)
    dst_context = Context(settings=dst_settings)

    update_stores(src_database, dst_database)
    update_categories(src_database, dst_database)
    update_articles(src_database, dst_database, dst_context)
