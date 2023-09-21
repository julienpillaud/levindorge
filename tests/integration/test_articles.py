import http
from typing import Any, Mapping
from unittest import mock

import pytest
from flask.testing import FlaskClient
from pymongo.database import Database
from pymongo.results import InsertOneResult

from tests.integration.data import article_data


@pytest.mark.parametrize("shop", ["angouleme", "sainte-eulalie", "pessac"])
def test_get_articles(
    client: FlaskClient,
    templates: list[tuple[Any, Any]],
    inserted_article: InsertOneResult,
    shop: str,
) -> None:
    response = client.get(f"/articles/beer?shop={shop}")
    assert response.status_code == http.HTTPStatus.OK

    assert len(templates) == 1
    template, context = templates[0]
    assert len(context["articles"]) == 1


@pytest.mark.parametrize("data", [article_data])
@mock.patch("application.use_cases.tactill.Tactill", mock.MagicMock())
def test_create_article(
    client: FlaskClient, database: Database[Mapping[str, Any]], data: dict[str, Any]
) -> None:
    response = client.post("/articles/create/beer", data=data)
    assert response.status_code == http.HTTPStatus.FOUND

    article = database.catalog.find_one({"name.name2": "TEST"})
    assert article
    assert article["type"] == "Bière"
    assert article["name"] == {"name1": "", "name2": "TEST"}
    assert article["buy_price"] == 1.5
    assert article["excise_duty"] == 0.2
    assert article["social_security_levy"] == 0.0
    assert article["tax"] == 20.0
    assert article["distributor"] == "Néodif"
    assert article["barcode"] == "000001"
    assert article["region"] == "France"
    assert article["color"] == "Blonde"
    assert article["taste"] == ""
    assert article["volume"] == 33.0
    assert article["alcohol_by_volume"] == 8.0
    assert article["packaging"] == 0
    assert article["deposit"] == {"unit": 0.0, "case": 0.0}
    assert article["food_pairing"] == []
    assert article["biodynamic"] == ""
    assert article["validated"] is False
    assert article["created_by"] == "User"
    assert article["shops"]["angouleme"] == {
        "sell_price": 3.5,
        "bar_price": 0.0,
        "stock_quantity": 0,
    }
    assert article["shops"]["sainte-eulalie"] == {
        "sell_price": 3.5,
        "bar_price": 0.0,
        "stock_quantity": 0,
    }
    assert article["shops"]["pessac"] == {
        "sell_price": 3.5,
        "bar_price": 5.0,
        "stock_quantity": 0,
    }


@pytest.mark.parametrize("data", [article_data])
@mock.patch("application.use_cases.tactill.Tactill", mock.MagicMock())
def test_update_article(
    client: FlaskClient,
    database: Database[Mapping[str, Any]],
    inserted_article: InsertOneResult,
    data: dict[str, Any],
) -> None:
    data["buy_price"] = 1.7
    data["sell_price_pessac"] = 3.9
    article_id = str(inserted_article.inserted_id)
    response = client.post(f"/articles/update/{article_id}", data=data)
    assert response.status_code == http.HTTPStatus.FOUND

    article = database.catalog.find_one({"name.name2": "TEST"})
    assert article
    assert article["type"] == "Bière"
    assert article["name"] == {"name1": "", "name2": "TEST"}
    assert article["buy_price"] == 1.7
    assert article["excise_duty"] == 0.2
    assert article["social_security_levy"] == 0.0
    assert article["tax"] == 20.0
    assert article["distributor"] == "Néodif"
    assert article["barcode"] == "000001"
    assert article["region"] == "France"
    assert article["color"] == "Blonde"
    assert article["taste"] == ""
    assert article["volume"] == 33.0
    assert article["alcohol_by_volume"] == 8.0
    assert article["packaging"] == 0
    assert article["deposit"] == {"unit": 0.0, "case": 0.0}
    assert article["food_pairing"] == []
    assert article["biodynamic"] == ""
    assert article["validated"] is False
    assert article["created_by"] == "User"
    assert article["shops"]["angouleme"] == {
        "sell_price": 3.9,
        "bar_price": 0.0,
        "stock_quantity": 0,
    }
    assert article["shops"]["sainte-eulalie"] == {
        "sell_price": 3.9,
        "bar_price": 0.0,
        "stock_quantity": 0,
    }
    assert article["shops"]["pessac"] == {
        "sell_price": 3.9,
        "bar_price": 5.0,
        "stock_quantity": 0,
    }


@mock.patch("application.use_cases.tactill.Tactill", mock.MagicMock())
def test_delete_article(
    client: FlaskClient,
    database: Database[Mapping[str, Any]],
    inserted_article: InsertOneResult,
) -> None:
    article_id = str(inserted_article.inserted_id)
    response = client.get(f"/articles/delete/{article_id}")
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
