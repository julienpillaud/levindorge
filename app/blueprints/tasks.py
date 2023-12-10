from flask import Blueprint, redirect, url_for
from flask_login import login_required

from app.worker import task_update_dashboard_stocks, task_update_wizishop_stocks


blueprint = Blueprint(name="tasks", import_name=__name__, url_prefix="/tasks")


@blueprint.get("/update_dashboard_stocks")
@login_required
def update_dashboard_stocks():
    task_update_dashboard_stocks.delay()
    return redirect(url_for("auth.home"))


@blueprint.get("/update_wizishop_stocks")
@login_required
def update_wizishop_stocks():
    task_update_wizishop_stocks.delay()
    return redirect(url_for("auth.home"))
