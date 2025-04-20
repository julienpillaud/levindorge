import os
from collections.abc import Iterator
from typing import Any

import jwt
import pytest
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database
from starlette.testclient import TestClient

from app.api.app import create_app
from app.api.dependencies import get_settings
from app.core.config import Settings

pytest_plugins = ["tests.fixtures.articles"]

load_dotenv()


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings(
        ENVIRONMENT="test",
        SECRET_KEY=os.environ["SECRET_KEY"],
        MONGODB_URI=os.environ["MONGODB_URI"],
        MONGODB_DATABASE="test",
        WIZISHOP_EMAIL="",
        WIZISHOP_PASSWORD="",
        CELERY_BROKER_URL="",
        CELERY_RESULT_BACKEND="",
        LOGFIRE_TOKEN="",
        LOGFIRE_SERVICE_NAME="",
    )


@pytest.fixture(scope="session")
def database(settings: Settings) -> Iterator[Database[dict[str, Any]]]:
    client = MongoClient(settings.MONGODB_URI)
    database = client[settings.MONGODB_DATABASE]
    yield database
    for collection in ["users", "articles"]:
        database[collection].delete_many({})
    client.close()


@pytest.fixture(scope="session")
def test_user(database: Database[dict[str, Any]]) -> dict[str, Any]:
    user_data = {
        "name": "Test",
        "username": "test_user",
        "email": "test@email.com",
        "password": "hashed_password",
        "role": "user",
        "shops": ["shop-test"],
    }
    database["users"].insert_one(user_data)
    return user_data


@pytest.fixture(scope="session")
def client(settings: Settings, test_user: dict[str, Any]) -> Iterator[TestClient]:
    token = jwt.encode(
        {"sub": test_user["email"]},
        os.environ["SECRET_KEY"],
        algorithm="HS256",
    )

    def get_settings_override() -> Settings:
        return settings

    app = create_app(settings=settings)

    app.dependency_overrides[get_settings] = get_settings_override
    yield TestClient(app, cookies={"access_token": f"Bearer {token}"})
    app.dependency_overrides.clear()
