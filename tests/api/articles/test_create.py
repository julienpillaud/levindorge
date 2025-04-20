import json
from typing import Any

import pytest
from pymongo.database import Database
from starlette import status
from starlette.testclient import TestClient


@pytest.mark.parametrize(
    "list_category, type_category",
    [
        ("beer", "Bière"),
        # ("cider", "Cidre"),
        # ("keg", "Fût"),
        # ("mini_keg", "Mini-fût"),
        # ("rhum", "Rhum"),
        # ("whisky", "Whisky"),
        # ("arranged", "Rhum arrangé"),
        # ("spirit", "Gin"),
        # ("wine", "Vin"),
        # ("fortified_wine", "Porto"),
        # ("sparkling_wine", "Vin effervescent"),
        # ("bib", "BIB"),
        # ("box", "Coffret"),
        # ("food", "Alimentation"),
        # ("misc", "Accessoire"),
    ],
)
def test_create(
    client: TestClient,
    database: Database[dict[str, Any]],
    article: dict[str, Any],
    list_category: str,
    type_category: str,
) -> None:
    article["type"] = type_category
    article["name2"] = f"Test {list_category}"
    article["bar_price_shop-test"] = 5
    article["sell_price_shop-test"] = 2.3
    article_volume = json.loads(article["volume"])

    response = client.post(f"/articles/create/{list_category}", data=article)
    assert response.status_code == status.HTTP_200_OK

    article_db = database["articles"].find_one({"name.name2": f"Test {list_category}"})
    assert article_db
    assert article_db["type"] == article["type"]
    assert article_db["name"] == {"name1": article["name1"], "name2": article["name2"]}
    assert article_db["buy_price"] == float(article["buy_price"])
    assert article_db["excise_duty"] == float(article["excise_duty"])
    assert article_db["social_security_levy"] == float(article["social_security_levy"])
    assert article_db["tax"] == float(article["tax"])
    assert article_db["distributor"] == article["distributor"]
    assert article_db["barcode"] == article["barcode"]
    assert article_db["region"] == article["region"]
    assert article_db["color"] == article["color"]
    assert article_db["taste"] == article["taste"]
    assert article_db["volume"] == article_volume
    assert article_db["alcohol_by_volume"] == float(article["alcohol_by_volume"])
    assert article_db["packaging"] == int(article["packaging"])
    assert article_db["deposit"] == {
        "unit": float(article["unit"]),
        "case": float(article["case"]),
    }
    assert article_db["food_pairing"] == []
    assert article_db["biodynamic"] == ""
    assert article_db["validated"] is False
    shops = article_db["shops"]
    assert shops["shop-test"]["bar_price"] == article["bar_price_shop-test"]
    assert shops["shop-test"]["sell_price"] == article["sell_price_shop-test"]
    assert shops["shop-test"]["stock_quantity"] == 0
