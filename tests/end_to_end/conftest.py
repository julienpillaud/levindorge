import os
from collections.abc import Iterator
from datetime import datetime, timezone
from typing import Any, Mapping

import pytest
from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.results import InsertOneResult
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
    mongo_uri = os.environ.get("MONGO_URI")
    client: MongoClient[Mapping[str, Any]] = MongoClient(mongo_uri)
    yield client.dashboard
    client.close()


@pytest.fixture
def created_article(database: Database[Mapping[str, Any]]) -> Iterator[InsertOneResult]:
    date = datetime.now(timezone.utc)
    price_data = {
        "sell_price": 3.5,
        "bar_price": 5.0,
        "stock_quantity": 0,
    }
    article_data = {
        "validated": False,
        "created_by": "Admin",
        "created_at": date,
        "updated_at": date,
        "distributor": "Néodif",
        "distributor_reference": "",
        "barcode": "",
        "reference": "",
        "buy_price": 1.5,
        "excise_duty": 0.2,
        "social_security_levy": 0.0,
        "tax": 20.0,
        "shops": {
            "angouleme": price_data,
            "sainte-eulalie": price_data,
            "pessac": price_data,
        },
        "type": "Bière",
        "name": {"name1": "", "name2": "TEST"},
        "volume": 33.0,
        "alcohol_by_volume": 8.0,
        "region": "France",
        "color": "Blonde",
        "taste": "",
        "packaging": 0,
        "deposit": {
            "unit": 0.0,
            "case": 0.0,
        },
        "food_pairing": [],
        "biodynamic": "",
    }
    result = database.catalog.insert_one(article_data)
    yield result
    database.catalog.delete_one({"_id": ObjectId(result.inserted_id)})


@pytest.fixture
def article_to_delete(database: Database[Mapping[str, Any]]) -> Iterator[list[str]]:
    to_delete: list[str] = []
    yield to_delete
    for article_id in to_delete:
        database.catalog.delete_one({"_id": ObjectId(article_id)})
