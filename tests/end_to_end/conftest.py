import os
from collections.abc import Iterator
from typing import Any, Mapping

import pytest
from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from app.entities.article import Article
from tests.data import article_to_insert

load_dotenv()


@pytest.fixture
def driver() -> Iterator[webdriver.Chrome]:
    options = Options()
    # options.add_argument("--headless=new")
    driver_ = webdriver.Chrome(options=options)
    driver_.get("http://127.0.0.1:5000")
    cookie = os.getenv("COOKIE")
    driver_.add_cookie({"name": "session", "value": cookie})
    yield driver_

    driver_.quit()


@pytest.fixture
def database() -> Iterator[Database[Mapping[str, Any]]]:
    uri = os.environ.get("MONGODB_URI")
    database = os.environ.get("MONGODB_DATABASE")
    client: MongoClient[Mapping[str, Any]] = MongoClient(uri)
    yield client[database]
    client.close()


@pytest.fixture
def inserted_article(database: Database[Mapping[str, Any]]) -> Iterator[Article]:
    result = database.catalog.insert_one(article_to_insert.model_dump())
    article_id = result.inserted_id
    yield Article(id=article_id, **article_to_insert.model_dump())
    database.catalog.delete_one({"_id": ObjectId(article_id)})


@pytest.fixture
def article_to_delete(database: Database[Mapping[str, Any]]) -> Iterator[list[str]]:
    to_delete: list[str] = []
    yield to_delete
    for article_id in to_delete:
        database.catalog.delete_one({"_id": ObjectId(article_id)})
