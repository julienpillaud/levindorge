from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import login_required

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
    items = ItemManager.list(repository=repository, category=category)

    return render_template(
        "item_list.html", title=title, category=category, items=items
    )


@blueprint.post("/<category>")
@login_required
def create_item(category: str):
    request_item = RequestItem(**request.form)

    repository = current_app.config["repository_provider"]()
    ItemManager.create(
        repository=repository, category=category, request_item=request_item
    )

    return redirect(url_for("items.get_items", category=category))


@blueprint.get("/<category>/<item_id>")
@login_required
def delete_item(category: str, item_id: str):
    repository = current_app.config["repository_provider"]()
    ItemManager.delete(repository=repository, category=category, item_id=item_id)

    return redirect(request.referrer)
