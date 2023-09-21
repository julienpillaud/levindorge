import os
from collections.abc import Iterator
from typing import Any, Mapping

import pytest
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, template_rendered
from flask.testing import FlaskClient
from flask_login import FlaskLoginClient
from pymongo import MongoClient
from pymongo.database import Database

from app import app
from application.blueprints.auth import Role, User
from application.entities.article import Article
from tests.integration.data import article_to_insert

load_dotenv()


@pytest.fixture
def flask_app() -> Flask:
    app.test_client_class = FlaskLoginClient
    app.config.update({"TESTING": True})
    return app


@pytest.fixture
def client(flask_app: Flask) -> FlaskClient:
    user = User(
        name="Test",
        username="test",
        email="user@levindorge.com",
        password="password",
        role=Role.USER,
        shops=["pessac"],
    )
    with flask_app.test_client(user=user) as client:
        return client


@pytest.fixture
def templates(flask_app: Flask) -> Iterator[list[tuple[Any, Any]]]:
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, flask_app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, flask_app)


@pytest.fixture
def database() -> Iterator[Database[Mapping[str, Any]]]:
    mongo_uri = os.environ.get("MONGO_URI")
    client: MongoClient[Mapping[str, Any]] = MongoClient(mongo_uri)
    yield client.dashboard
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
