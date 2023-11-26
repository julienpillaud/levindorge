import logging
import os
from datetime import datetime, timezone
from typing import Any

import rollbar
import rollbar.contrib.flask
from flask import Flask, got_request_exception, render_template
from flask_login import current_user
from zoneinfo import ZoneInfo

from app.blueprints import articles as articles_blueprint
from app.blueprints import auth as auth_blueprint
from app.blueprints import inventory as inventory_blueprint
from app.blueprints import items as items_blueprint
from app.blueprints import tags as tags_blueprint
from app.config import settings
from app.data import navbar_categories
from app.repository.dependencies import repository_provider

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.config["repository_provider"] = repository_provider

auth_blueprint.login_manager.init_app(app)
auth_blueprint.bcrypt.init_app(app)

app.register_blueprint(auth_blueprint.blueprint)
app.register_blueprint(articles_blueprint.blueprint)
app.register_blueprint(items_blueprint.blueprint)
app.register_blueprint(inventory_blueprint.blueprint)
app.register_blueprint(tags_blueprint.blueprint)


with app.app_context():
    rollbar.init(
        access_token=settings.ROLLBAR_ACCESS_TOKEN,
        environment=settings.ENVIRONMENT,
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False,
    )

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


if settings.ENVIRONMENT == "production":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


@app.errorhandler(401)
def error_page(error):
    return render_template("error.html"), error.code


@app.context_processor
def register_context() -> dict[str, Any]:
    context: dict[str, Any] = {"navbar_categories": navbar_categories}

    repository = repository_provider()
    user_shops = repository.get_user_shops(user_shops=current_user.shops)
    context["user_shops"] = user_shops

    return context


@app.template_filter()
def strip_zeros(value: float) -> str:
    return str(value).rstrip("0").rstrip(".")


@app.template_filter()
def local_timezone(value: datetime) -> datetime:
    return value.replace(tzinfo=timezone.utc).astimezone(tz=ZoneInfo("Europe/Paris"))


@app.template_filter()
def get_navbar_category_title(list_category: str) -> str:
    for _, categories in navbar_categories.items():
        for category in categories:
            if category.code == list_category:
                return category.plural_name
    return list_category


@app.route("/demo")
def demo() -> str:
    list_category = "beer"
    repository = repository_provider()

    current_shop = repository.get_shop_by_username(username="pessac")
    articles = repository.get_articles_by_list(list_category)

    return render_template(
        "demo_list.html",
        current_shop=current_shop,
        list_category=list_category,
        articles=articles,
    )
