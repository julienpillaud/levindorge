from flask import Blueprint, redirect, url_for
from flask_login import login_required

from app.worker import (
    update_stocks,
    clean_tactill,
    update_tactill,
)


blueprint = Blueprint(name="tasks", import_name=__name__, url_prefix="/tasks")


@blueprint.get("/update_stocks")
@login_required
def task_update_stocks():
    update_stocks.delay()
    return redirect(url_for("auth.home"))


@blueprint.get("/clean_tactill")
@login_required
def task_clean_tactill():
    clean_tactill.delay()
    return redirect(url_for("auth.home"))


@blueprint.get("/update_tactill")
@login_required
def task_update_tactill():
    update_tactill.delay()
    return redirect(url_for("auth.home"))
