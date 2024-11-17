import http
from collections.abc import Mapping
from typing import Any

import pytest
from flask.testing import FlaskClient
from pymongo.database import Database


@pytest.mark.parametrize(
    "category", ["breweries", "distilleries", "distributors", "countries", "regions"]
)
def test_get_items(
    client: FlaskClient,
    templates: list[tuple[Any, Any]],
    category: str,
) -> None:
    response = client.get(f"/items/{category}")
    assert response.status_code == http.HTTPStatus.OK

    assert len(templates) == 1
    template, context = templates[0]
    assert context["title"]
    assert context["category"] == category
    assert len(context["items"]) >= 1


@pytest.mark.parametrize(
    "category", ["breweries", "distilleries", "distributors", "countries", "regions"]
)
def test_create_items(
    client: FlaskClient, database: Database[Mapping[str, Any]], category: str
) -> None:
    data = {"name": "TEST"}
    response = client.post(f"/items/{category}", data=data)
    assert response.status_code == http.HTTPStatus.FOUND

    collection = database.get_collection(name=category)
    item = collection.find_one(data)
    assert item
    assert item["name"] == "TEST"

    collection.delete_one(data)
