import time
from typing import Any, Mapping

import pytest
from bson import ObjectId
from pymongo.database import Database
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from application.entities.article import Article, CreateOrUpdateArticle
from tests.data import article_to_insert


def strip_zeros(value: float) -> str:
    return str(value).rstrip("0").rstrip(".")


@pytest.mark.parametrize("data", [article_to_insert])
def test_create_article(
    driver: webdriver.Chrome,
    database: Database[Mapping[str, Any]],
    data: CreateOrUpdateArticle,
    article_to_delete: list[str],
) -> None:
    # Given: we navigate to the page to create a new article
    url = "http://127.0.0.1:5000/articles/create/beer"
    driver.get(url)

    # When: we fill all the necessary fields
    driver.find_element(by=By.NAME, value="name2").send_keys(data.name.name2)
    Select(driver.find_element(by=By.NAME, value="region")).select_by_visible_text(
        data.region
    )
    Select(driver.find_element(by=By.NAME, value="color")).select_by_visible_text(
        data.color
    )
    Select(driver.find_element(by=By.NAME, value="volume")).select_by_visible_text(
        strip_zeros(data.volume)
    )
    driver.find_element(by=By.NAME, value="alcohol_by_volume").send_keys(
        data.alcohol_by_volume
    )
    driver.find_element(by=By.NAME, value="buy_price").send_keys(data.buy_price)
    driver.find_element(by=By.NAME, value="excise_duty").send_keys(data.excise_duty)
    driver.find_element(by=By.NAME, value="bar_price_pessac").send_keys(
        data.shops["pessac"].bar_price
    )
    Select(driver.find_element(by=By.NAME, value="distributor")).select_by_visible_text(
        data.distributor
    )
    driver.find_element(by=By.NAME, value="barcode").send_keys(data.barcode)
    Select(driver.find_element(by=By.NAME, value="unit")).select_by_visible_text(
        strip_zeros(data.deposit.unit)
    )
    Select(driver.find_element(by=By.NAME, value="case")).select_by_visible_text(
        strip_zeros(data.deposit.case)
    )
    Select(driver.find_element(by=By.NAME, value="packaging")).select_by_visible_text(
        str(data.packaging)
    )

    # And: we click on the 'create' button
    button = driver.find_element(by=By.NAME, value="create")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
    button.click()

    WebDriverWait(driver, 20).until(EC.url_changes(url))

    # Then: the article in the database is created
    article = database.catalog.find_one({"name.name2": data.name.name2})
    assert article
    article_to_delete.append(article["_id"])

    assert article["type"] == data.type
    assert article["name"]["name1"] == data.name.name1
    assert article["name"]["name2"] == data.name.name2
    assert article["buy_price"] == data.buy_price
    assert article["excise_duty"] == data.excise_duty
    assert article["social_security_levy"] == data.social_security_levy
    assert article["tax"] == data.tax
    assert article["distributor"] == data.distributor
    assert article["barcode"] == data.barcode
    assert article["region"] == data.region
    assert article["color"] == data.color
    assert article["taste"] == data.taste
    assert article["volume"] == data.volume
    assert article["alcohol_by_volume"] == data.alcohol_by_volume
    assert article["packaging"] == data.packaging
    assert article["deposit"]["unit"] == data.deposit.unit
    assert article["deposit"]["unit"] == data.deposit.case
    assert article["food_pairing"] == data.food_pairing
    assert article["biodynamic"] == data.biodynamic

    assert (
        article["shops"]["angouleme"]["sell_price"]
        == data.shops["angouleme"].sell_price
    )
    assert (
        article["shops"]["angouleme"]["bar_price"] == data.shops["angouleme"].bar_price
    )
    assert (
        article["shops"]["angouleme"]["bar_price"]
        == data.shops["angouleme"].stock_quantity
    )

    assert (
        article["shops"]["sainte-eulalie"]["sell_price"]
        == data.shops["sainte-eulalie"].sell_price
    )
    assert (
        article["shops"]["sainte-eulalie"]["bar_price"]
        == data.shops["sainte-eulalie"].bar_price
    )
    assert (
        article["shops"]["sainte-eulalie"]["stock_quantity"]
        == data.shops["sainte-eulalie"].stock_quantity
    )

    assert article["shops"]["pessac"]["sell_price"] == data.shops["pessac"].sell_price
    assert article["shops"]["pessac"]["bar_price"] == data.shops["pessac"].bar_price
    assert (
        article["shops"]["pessac"]["stock_quantity"]
        == data.shops["pessac"].stock_quantity
    )


def test_delete_article(
    driver: webdriver.Chrome,
    database: Database[Mapping[str, Any]],
    inserted_article: Article,
) -> None:
    # Given: we navigate to the page of article list
    driver.get("http://127.0.0.1:5000/articles/beer?shop=angouleme")

    # When: we click on the 'delete' button
    href = f"/articles/delete/{inserted_article.id}"
    driver.find_element(By.XPATH, f"//a[@href='{href}']").click()

    # Then: the article in the database doesn't exist anymore
    article = database.catalog.find_one({"_id": ObjectId(inserted_article.id)})
    assert article is None


def test_validate_article(
    driver: webdriver.Chrome,
    database: Database[Mapping[str, Any]],
    inserted_article: Article,
) -> None:
    # Given: we navigate to the page of articles to validate
    driver.get("http://127.0.0.1:5000/articles/validate")

    # When: we click on the 'validate' button
    href = f"/articles/validate/{inserted_article.id}"
    driver.find_element(By.XPATH, f"//a[@href='{href}']").click()

    # Then: the article in the database is validated
    article = database.catalog.find_one({"_id": ObjectId(inserted_article.id)})
    assert article
    assert article["validated"] is True


def test_update_article(
    driver: webdriver.Chrome,
    database: Database[Mapping[str, Any]],
    inserted_article: Article,
) -> None:
    article_id = inserted_article.id
    new_buy_price = 1.7
    new_recommended_price = 3.9

    # Given: we navigate to the page to update the article
    url = f"http://127.0.0.1:5000/articles/update/{article_id}"
    driver.get(url)

    # When: we update the 'buy price' field
    excise_duty = driver.find_element(by=By.NAME, value="buy_price")
    excise_duty.clear()
    excise_duty.send_keys(new_buy_price)

    # TODO: best way to trigger the js ?
    excise_duty.send_keys(Keys.UP)
    excise_duty.send_keys(Keys.DOWN)
    time.sleep(1)

    driver.find_element(by=By.NAME, value="update").click()
    WebDriverWait(driver, 20).until(EC.url_changes(url))

    # Then: the article in the database is updated
    article = database.catalog.find_one({"_id": ObjectId(article_id)})
    assert article
    assert article["updated_at"] > article["created_at"]
    assert article["buy_price"] == new_buy_price
    assert article["shops"]["angouleme"]["sell_price"] == new_recommended_price
    assert article["shops"]["sainte-eulalie"]["sell_price"] == new_recommended_price
    assert article["shops"]["pessac"]["sell_price"] == new_recommended_price


def test_update_and_validate_article(
    driver: webdriver.Chrome,
    database: Database[Mapping[str, Any]],
    inserted_article: Article,
) -> None:
    article_id = inserted_article.id
    new_buy_price = 1.7
    new_recommended_price = 3.9

    # Given: we navigate to the page to update and validate the article
    url = f"http://127.0.0.1:5000/articles/update/{article_id}?validate=True"
    driver.get(url)

    # When: we update the 'buy price' field
    excise_duty = driver.find_element(by=By.NAME, value="buy_price")
    excise_duty.clear()
    excise_duty.send_keys(new_buy_price)

    # TODO: best way to trigger the js ?
    excise_duty.send_keys(Keys.UP)
    excise_duty.send_keys(Keys.DOWN)
    time.sleep(1)

    driver.find_element(by=By.NAME, value="update").click()
    WebDriverWait(driver, 20).until(EC.url_changes(url))

    # Then: the article in the database is validated and updated
    article = database.catalog.find_one({"_id": ObjectId(article_id)})
    assert article
    assert article["validated"] is True
    assert article["updated_at"] > article["created_at"]
    assert article["buy_price"] == new_buy_price
    assert article["shops"]["angouleme"]["sell_price"] == new_recommended_price
    assert article["shops"]["sainte-eulalie"]["sell_price"] == new_recommended_price
    assert article["shops"]["pessac"]["sell_price"] == new_recommended_price
