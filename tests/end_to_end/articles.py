from typing import Any, Mapping

from bson import ObjectId
from pymongo.database import Database
from pymongo.results import InsertOneResult
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


def test_create_article(
    driver: webdriver.Chrome,
    database: Database[Mapping[str, Any]],
    article_to_delete: list[str],
) -> None:
    url = "http://127.0.0.1:5000/articles/create/beer"

    driver.get(url)
    driver.find_element(by=By.NAME, value="name2").send_keys("TEST")
    Select(driver.find_element(by=By.NAME, value="region")).select_by_visible_text(
        "France"
    )
    Select(driver.find_element(by=By.NAME, value="color")).select_by_visible_text(
        "Blonde"
    )
    Select(driver.find_element(by=By.NAME, value="volume")).select_by_visible_text("33")
    driver.find_element(by=By.NAME, value="alcohol_by_volume").send_keys("8")
    driver.find_element(by=By.NAME, value="buy_price").send_keys("1,5")
    driver.find_element(by=By.NAME, value="excise_duty").send_keys("0,2")
    Select(driver.find_element(by=By.NAME, value="distributor")).select_by_visible_text(
        "Néodif"
    )
    Select(driver.find_element(by=By.NAME, value="unit")).select_by_visible_text("0")
    Select(driver.find_element(by=By.NAME, value="case")).select_by_visible_text("0")
    Select(driver.find_element(by=By.NAME, value="packaging")).select_by_visible_text(
        "0"
    )

    # wait for create button to be clickable
    button = driver.find_element(by=By.NAME, value="create")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
    button.click()

    WebDriverWait(driver, 20).until(EC.url_changes(url))

    article = database.catalog.find_one({"name.name2": "TEST"})
    assert article
    article_to_delete.append(article["_id"])

    assert article["name"]["name1"] == ""
    assert article["name"]["name2"] == "TEST"
    assert article["distributor"] == "Néodif"
    assert article["distributor_reference"] == ""
    assert article["barcode"] == ""
    assert article["reference"] == ""
    assert article["buy_price"] == 1.5
    assert article["excise_duty"] == 0.2
    assert article["social_security_levy"] == 0.0
    assert article["tax"] == 20.0
    assert article["shops"] == {
        "angouleme": {
            "sell_price": 3.5,
            "bar_price": 0.0,
            "stock_quantity": 0,
        },
        "sainte-eulalie": {
            "sell_price": 3.5,
            "bar_price": 0.0,
            "stock_quantity": 0,
        },
        "pessac": {
            "sell_price": 3.5,
            "bar_price": 0.0,
            "stock_quantity": 0,
        },
    }
    assert article["type"] == "Bière"
    assert article["name"] == {"name1": "", "name2": "TEST"}
    assert article["volume"] == 33.0
    assert article["alcohol_by_volume"] == 8.0
    assert article["region"] == "France"
    assert article["color"] == "Blonde"
    assert article["taste"] == ""
    assert article["packaging"] == 0
    assert article["deposit"] == {"unit": 0.0, "case": 0.0}
    assert article["food_pairing"] == []
    assert article["biodynamic"] == ""


def test_update_article(
    driver: webdriver.Chrome,
    database: Database[Mapping[str, Any]],
    created_article: InsertOneResult,
) -> None:
    driver.get(f"http://127.0.0.1:5000/articles/update/{created_article.inserted_id}")
    excise_duty = driver.find_element(by=By.NAME, value="excise_duty")
    excise_duty.clear()
    excise_duty.send_keys(0.3)
    driver.find_element(by=By.NAME, value="update").click()

    article = database.catalog.find_one({"_id": ObjectId(created_article.inserted_id)})
    assert article
    assert article["updated_at"] > article["created_at"]
    assert article["excise_duty"] == 0.3


def test_delete_article(
    driver: webdriver.Chrome,
    database: Database[Mapping[str, Any]],
    created_article: InsertOneResult,
) -> None:
    driver.get("http://127.0.0.1:5000/articles/beer?shop=angouleme")
    href = f"/articles/delete/{created_article.inserted_id}"
    driver.find_element(By.XPATH, f"//a[@href='{href}']").click()

    article = database.catalog.find_one({"_id": ObjectId(created_article.inserted_id)})
    assert article is None
