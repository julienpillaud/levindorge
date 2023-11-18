from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required
from pydantic import ValidationError

from application.entities.inventory import RequestResetStocks
from application.use_cases.articles import ArticleManager
from application.use_cases.inventory import InventoryManager
from application.use_cases.tactill import TactillManager

blueprint = Blueprint(name="inventory", import_name=__name__, url_prefix="/inventory")


@blueprint.get("/")
@login_required
def get_inventories() -> str:
    repository = current_app.config["repository_provider"]()
    inventories = InventoryManager.get_inventories(repository=repository)
    return render_template("inventory_list.html", inventories=inventories)


@blueprint.post("/")
@login_required
def save_inventory():
    repository = current_app.config["repository_provider"]()

    request_shop = request.form["shop"]
    current_shop = repository.get_shop_by_username(username=request_shop)

    articles = ArticleManager.get(repository=repository)
    tactill_articles = TactillManager.get(shop=current_shop)
    InventoryManager.save(
        repository=repository,
        shop=current_shop,
        articles=articles,
        tactill_articles=tactill_articles,
    )

    return redirect(url_for("inventory.get_inventories"))


@blueprint.get("/<inventory_id>")
@login_required
def get_inventory(inventory_id: str) -> str:
    repository = current_app.config["repository_provider"]()
    inventory = InventoryManager.get_inventory(
        repository=repository, inventory_id=inventory_id
    )
    inventory_records = InventoryManager.get_inventory_records(
        repository=repository, inventory_id=inventory_id
    )
    return render_template(
        "inventory.html", inventory=inventory, inventory_records=inventory_records
    )


@blueprint.get("/delete/<inventory_id>")
@login_required
def delete_inventory(inventory_id: str):
    repository = current_app.config["repository_provider"]()
    InventoryManager.delete(repository=repository, inventory_id=inventory_id)
    return redirect(url_for("inventory.get_inventories"))


@blueprint.post("/stocks/reset")
@login_required
def reset_tactill_stocks():
    try:
        request_data = RequestResetStocks.model_validate(request.form.to_dict())
    except ValidationError:
        flash("Tu dois sélectionner un magasin !", "warning")
        return redirect(url_for("inventory.get_inventories"))

    repository = current_app.config["repository_provider"]()

    current_shop = repository.get_shop_by_username(username=request_data.shop)
    TactillManager.reset_stock(
        shop=current_shop, request_category=request_data.category
    )

    flash("Les stocks ont bien été remis à zéro !", "success")
    return redirect(url_for("inventory.get_inventories"))
