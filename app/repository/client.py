from typing import Any, Mapping

from pymongo import MongoClient
from pymongo.database import Database

from app.config import settings

client: MongoClient[Mapping[str, Any]] = MongoClient(settings.MONGODB_URI)
database: Database[Mapping[str, Any]] = client[settings.MONGODB_DATABASE]
