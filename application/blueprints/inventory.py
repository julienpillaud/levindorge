from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from application.entities.inventory import CreateOrUpdateInventory, RequestInventory
from utils import mongo_db

blueprint = Blueprint(name="inventory", import_name=__name__, url_prefix="/inventory")


@blueprint.get("/")
@login_required
def get_inventory():
    articles = mongo_db.get_articles_for_inventory()
    return render_template("inventory.html", articles_inventory=articles)


@blueprint.post("/save")
@login_required
def save_inventory():
    article_id = request.json.get("articleId")
    stock_quantity = request.json.get("stockQuantity")
    request_inventory = RequestInventory(
        article_id=article_id, stock_quantity=stock_quantity
    )

    article = mongo_db.get_article_by_id(request_inventory.article_id)

    sale_value = round(request_inventory.stock_quantity * article.taxfree_price, 2)
    deposit_value = 0
    if article.packaging > 0:
        deposit_value = round(
            (request_inventory.stock_quantity / article.packaging)
            * article.deposit.case,
            2,
        )

    inventory_record = CreateOrUpdateInventory(
        article_id=request_inventory.article_id,
        stock_quantity=request_inventory.stock_quantity,
        sale_value=sale_value,
        deposit_value=deposit_value,
    )
    mongo_db.save_inventory_record(inventory_record=inventory_record)

    return inventory_record.model_dump()


@blueprint.get("/reset")
@login_required
def reset_inventory():
    mongo_db.reset_inventory()
    return redirect(url_for("inventory.get_inventory"))
