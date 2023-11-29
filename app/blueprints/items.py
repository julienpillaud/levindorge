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

from app.entities.deposit import RequestDeposit
from app.entities.item import RequestItem
from app.use_cases.items import ItemManager

blueprint = Blueprint(name="items", import_name=__name__, url_prefix="/items")

item_titles = {
    "breweries": "Brasserie",
    "distilleries": "Distillerie",
    "distributors": "Fournisseur",
    "countries": "Pays",
    "regions": "Région",
}


@blueprint.get("/<category>")
@login_required
def get_items(category: str) -> str:
    title = item_titles.get(category, "Item")

    repository = current_app.config["repository_provider"]()
    items = ItemManager.get_items(repository=repository, category=category)

    return render_template(
        "item_list.html", title=title, category=category, items=items
    )


@blueprint.post("/<category>")
@login_required
def create_item(category: str):
    request_item = RequestItem(**request.form)

    repository = current_app.config["repository_provider"]()
    ItemManager.create_item(
        repository=repository, category=category, request_item=request_item
    )

    return redirect(url_for("items.get_items", category=category))


@blueprint.get("/<category>/<item_id>")
@login_required
def delete_item(category: str, item_id: str):
    repository = current_app.config["repository_provider"]()
    ItemManager.delete_item(repository=repository, category=category, item_id=item_id)

    return redirect(request.referrer)


@blueprint.get("/deposit")
@login_required
def get_deposits() -> str:
    repository = current_app.config["repository_provider"]()
    deposits = ItemManager.get_deposits(repository=repository)
    return render_template("deposits.html", deposits=deposits)


@blueprint.post("/deposit")
@login_required
def create_deposit():
    request_deposit = RequestDeposit.model_validate(request.form.to_dict())

    repository = current_app.config["repository_provider"]()
    ItemManager.create_deposit(repository=repository, request_deposit=request_deposit)

    return redirect(url_for("items.get_deposits"))


@blueprint.get("/deposit/<deposit_id>")
@login_required
def delete_deposit(deposit_id: str):
    repository = current_app.config["repository_provider"]()
    result = ItemManager.delete_deposit(repository=repository, deposit_id=deposit_id)
    if not result:
        flash(
            "La consigne ne peut pas être supprimée",
            "warning",
        )

    return redirect(request.referrer)
