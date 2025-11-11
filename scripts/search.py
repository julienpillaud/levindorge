from pymongo import MongoClient

from app.core.config import Settings
from app.infrastructure.repository.articles import ArticleRepository

settings = Settings()
client = MongoClient(settings.mongo_uri)
database = client[settings.mongo_database]
repo = ArticleRepository(database)
