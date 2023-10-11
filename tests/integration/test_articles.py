import http
from typing import Any, Mapping
from unittest import mock

import pytest
from bson import ObjectId
from flask.testing import FlaskClient
from pymongo.database import Database

from application.entities.article import Article
from tests.data import article_data, categories_for_list_view


@pytest.mark.parametrize("shop", ["angouleme", "sainte-eulalie", "pessac"])
def test_get_articles(
    client: FlaskClient,
    templates: list[tuple[Any, Any]],
    shop: str,
) -> None:
    list_category = "beer"
    response = client.get(f"/articles/{list_category}?shop={shop}")
    assert response.status_code == http.HTTPStatus.OK

    assert len(templates) == 1
    template, context = templates[0]
    assert context["current_shop"]
    assert context["list_category"] == list_category
    assert context["articles"]


@pytest.mark.parametrize("list_category", categories_for_list_view)
def test_create_article_view(
    client: FlaskClient, templates: list[tuple[Any, Any]], list_category: str
) -> None:
    response = client.get(f"/articles/create/{list_category}")
    assert response.status_code == http.HTTPStatus.OK

    assert len(templates) == 1
    template, context = templates[0]
    assert context["list_category"] == list_category
    assert context["ratio_category"]
    assert context["type_list"]


@pytest.mark.parametrize("data", [article_data])
@mock.patch("application.use_cases.tactill.Tactill", mock.MagicMock())
def test_create_article(
    client: FlaskClient,
    database: Database[Mapping[str, Any]],
    data: dict[str, Any],
    article_to_delete: list[str],
) -> None:
    recommended_price = 3.5

    response = client.post("/articles/create/beer", data=data)
    assert response.status_code == http.HTTPStatus.FOUND

    article = database.catalog.find_one({"name.name2": "TEST"})
    assert article
    article_to_delete.append(article["_id"])

    assert article["type"] == article_data["type"]
    assert article["name"]["name1"] == article_data["name1"]
    assert article["name"]["name2"] == article_data["name2"]
    assert article["buy_price"] == article_data["buy_price"]
    assert article["excise_duty"] == article_data["excise_duty"]
    assert article["social_security_levy"] == article_data["social_security_levy"]
    assert article["tax"] == article_data["tax"]
    assert article["distributor"] == article_data["distributor"]
    assert article["barcode"] == article_data["barcode"]
    assert article["region"] == article_data["region"]
    assert article["color"] == article_data["color"]
    assert article["taste"] == ""
    assert article["volume"] == article_data["volume"]
    assert article["alcohol_by_volume"] == article_data["alcohol_by_volume"]
    assert article["packaging"] == article_data["packaging"]
    assert article["deposit"]["unit"] == article_data["unit"]
    assert article["deposit"]["case"] == article_data["case"]
    assert article["food_pairing"] == []
    assert article["biodynamic"] == ""
    assert article["validated"] is False
    assert article["created_by"] == "User"

    sell_price = article_data["sell_price_pessac"]
    assert article["shops"]["angouleme"]["sell_price"] == recommended_price
    assert article["shops"]["sainte-eulalie"]["sell_price"] == recommended_price
    assert article["shops"]["pessac"]["sell_price"] == sell_price

    bar_price = article_data["bar_price_pessac"]
    assert article["shops"]["angouleme"]["bar_price"] == 0.0
    assert article["shops"]["sainte-eulalie"]["bar_price"] == 0.0
    assert article["shops"]["pessac"]["bar_price"] == bar_price

    assert article["shops"]["angouleme"]["stock_quantity"] == 0
    assert article["shops"]["sainte-eulalie"]["stock_quantity"] == 0
    assert article["shops"]["pessac"]["stock_quantity"] == 0


def test_update_article_view(
    client: FlaskClient, inserted_article: Article, templates: list[tuple[Any, Any]]
) -> None:
    article_id = inserted_article.id
    response = client.get(f"/articles/update/{article_id}")
    assert response.status_code == http.HTTPStatus.OK

    assert len(templates) == 1
    template, context = templates[0]
    assert context["article"]
    assert context["list_category"]
    assert context["ratio_category"]


@pytest.mark.parametrize("data", [article_data])
@mock.patch("application.use_cases.tactill.Tactill", mock.MagicMock())
def test_update_article(
    client: FlaskClient,
    database: Database[Mapping[str, Any]],
    inserted_article: Article,
    data: dict[str, Any],
) -> None:
    data["buy_price"] = 1.7
    new_recommended_price = 3.9
    data["sell_price_pessac"] = 4.0

    article_id = inserted_article.id
    response = client.post(f"/articles/update/{article_id}", data=data)
    assert response.status_code == http.HTTPStatus.FOUND

    article = database.catalog.find_one({"_id": ObjectId(article_id)})
    assert article
    assert article["type"] == inserted_article.type
    assert article["name"]["name1"] == inserted_article.name.name1
    assert article["name"]["name2"] == inserted_article.name.name2
    assert article["buy_price"] == data["buy_price"]
    assert article["excise_duty"] == inserted_article.excise_duty
    assert article["social_security_levy"] == inserted_article.social_security_levy
    assert article["tax"] == inserted_article.tax
    assert article["distributor"] == inserted_article.distributor
    assert article["barcode"] == inserted_article.barcode
    assert article["region"] == inserted_article.region
    assert article["color"] == inserted_article.color
    assert article["taste"] == inserted_article.taste
    assert article["volume"] == inserted_article.volume
    assert article["alcohol_by_volume"] == inserted_article.alcohol_by_volume
    assert article["packaging"] == inserted_article.packaging
    assert article["deposit"]["unit"] == inserted_article.deposit.unit
    assert article["deposit"]["case"] == inserted_article.deposit.case
    assert article["food_pairing"] == inserted_article.food_pairing
    assert article["biodynamic"] == inserted_article.biodynamic
    assert article["validated"] == inserted_article.validated
    assert article["created_by"] == inserted_article.created_by

    assert article["shops"]["angouleme"]["sell_price"] == new_recommended_price
    assert article["shops"]["sainte-eulalie"]["sell_price"] == new_recommended_price
    assert article["shops"]["pessac"]["sell_price"] == data["sell_price_pessac"]

    assert (
        article["shops"]["angouleme"]["bar_price"]
        == inserted_article.shops["angouleme"].bar_price
    )
    assert (
        article["shops"]["sainte-eulalie"]["bar_price"]
        == inserted_article.shops["sainte-eulalie"].bar_price
    )
    assert (
        article["shops"]["pessac"]["bar_price"]
        == inserted_article.shops["pessac"].bar_price
    )
    assert (
        article["shops"]["angouleme"]["stock_quantity"]
        == inserted_article.shops["angouleme"].stock_quantity
    )
    assert (
        article["shops"]["sainte-eulalie"]["stock_quantity"]
        == inserted_article.shops["sainte-eulalie"].stock_quantity
    )
    assert (
        article["shops"]["pessac"]["stock_quantity"]
        == inserted_article.shops["pessac"].stock_quantity
    )


@mock.patch("application.use_cases.tactill.Tactill", mock.MagicMock())
def test_delete_article(
    client: FlaskClient,
    database: Database[Mapping[str, Any]],
    inserted_article: Article,
) -> None:
    article_id = inserted_article.id
    response = client.get(f"/articles/delete/{article_id}")
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


def test_validate_articles(client: FlaskClient):
    response = client.get("/articles/validate")
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
