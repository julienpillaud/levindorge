from typing import Any

from flask import Flask, render_template
from flask_login import current_user

from application.blueprints import articles as articles_blueprint
from application.blueprints import auth as auth_blueprint
from application.blueprints import inventory as inventory_blueprint
from application.blueprints import items as items_blueprint
from application.blueprints import tags as tags_blueprint
from application.config import settings
from application.repository.dependencies import repository_provider

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


@app.errorhandler(401)
def error_page(error):
    return render_template("error.html"), error.code


@app.context_processor
def register_user_shops() -> dict[str, Any]:
    if current_user.is_authenticated:
        repository = repository_provider()
        user_shops = repository.get_user_shops(user_shops=current_user.shops)

        return {"user_shops": user_shops}

    return {}


@app.template_filter()
def strip_zeros(value: float) -> str:
    return str(value).rstrip("0").rstrip(".")


@app.route("/demo")
def demo() -> str:
    repository = repository_provider()
    articles = repository.get_articles_by_list("beer")

    return render_template("demo_list.html", shop="pessac", articles=articles[:100])
