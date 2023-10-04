from typing import Any

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from application.entities.inventory import RequestInventory
from application.use_cases.inventory import InventoryManager
from utils import mongo_db

blueprint = Blueprint(name="inventory", import_name=__name__, url_prefix="/inventory")


@blueprint.get("/")
@login_required
def get_inventory() -> str:
    articles = mongo_db.get_articles_for_inventory()
    return render_template("inventory.html", articles_inventory=articles)


@blueprint.post("/save")
@login_required
def save_inventory() -> dict[str, Any]:
    article_id = request.json.get("articleId")
    stock_quantity = request.json.get("stockQuantity")
    request_inventory = RequestInventory(
        article_id=article_id, stock_quantity=stock_quantity
    )

    inventory_record = InventoryManager.save(request_inventory=request_inventory)

    return inventory_record.model_dump()


@blueprint.get("/reset")
@login_required
def reset_inventory():
    InventoryManager.reset()
    return redirect(url_for("inventory.get_inventory"))
