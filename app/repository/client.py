from collections.abc import Mapping
from functools import lru_cache
from typing import Any

from pymongo import MongoClient
from pymongo.database import Database

from app.config import settings


@lru_cache(maxsize=1)
def get_database() -> Database[Mapping[str, Any]]:
    client: MongoClient[Mapping[str, Any]] = MongoClient(settings.MONGODB_URI)
    return client[settings.MONGODB_DATABASE]
