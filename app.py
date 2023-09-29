from flask import Flask, render_template

from application.blueprints import articles as articles_blueprint
from application.blueprints import auth as auth_blueprint
from application.blueprints import inventory as inventory_blueprint
from application.blueprints import items as items_blueprint
from application.blueprints import tags as tags_blueprint
from utils import mongo_db

app = Flask(__name__)
app.secret_key = "some_secret"

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
def post_shops_margins():
    shops_margins = mongo_db.get_shops_margins()
    return {"shops_margins": shops_margins}


@app.template_filter()
def strip_zeros(value):
    return str(value).rstrip("0").rstrip(".")


@app.route("/demo")
def demo():
    articles = mongo_db.get_articles_by_list("beer")
    return render_template("demo_list.html", shop="pessac", articles=articles[:100])
