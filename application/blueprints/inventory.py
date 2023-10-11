from typing import Any

from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import login_required

from application.entities.inventory import RequestInventory
from application.use_cases.inventory import InventoryManager

blueprint = Blueprint(name="inventory", import_name=__name__, url_prefix="/inventory")


@blueprint.get("/")
@login_required
def get_inventory() -> str:
    repository = current_app.config["repository_provider"]()
    articles = repository.get_articles_for_inventory()

    return render_template("inventory.html", articles_inventory=articles)


@blueprint.post("/save")
@login_required
def save_inventory() -> dict[str, Any]:
    article_id = request.json.get("articleId")
    stock_quantity = request.json.get("stockQuantity")
    request_inventory = RequestInventory(
        article_id=article_id, stock_quantity=stock_quantity
    )

    repository = current_app.config["repository_provider"]()
    inventory_record = InventoryManager.save(
        repository=repository, request_inventory=request_inventory
    )

    return inventory_record.model_dump()


@blueprint.get("/reset")
@login_required
def reset_inventory():
    repository = current_app.config["repository_provider"]()
    InventoryManager.reset(repository=repository)

    return redirect(url_for("inventory.get_inventory"))
