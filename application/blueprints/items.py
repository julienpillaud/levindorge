from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from application.entities.item import RequestItem
from utils import mongo_db

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
def get_items(category: str):
    items = mongo_db.get_items(category=category)
    title = item_titles.get(category, "Item")
    return render_template(
        "item_list.html", title=title, category=category, items=items
    )


@blueprint.post("/<category>")
@login_required
def create_item(category: str):
    request_form = request.form.to_dict()
    item = RequestItem(**request_form)
    mongo_db.create_item(category=category, item=item)
    return redirect(url_for("items.get_items", category=category))


@blueprint.get("/<category>/<item_id>")
@login_required
def delete_item(category: str, item_id: str):
    mongo_db.delete_item(category=category, item_id=item_id)
    return redirect(request.referrer)
