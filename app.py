import os

from flask import Flask, redirect, render_template, request, url_for
from flask_login import login_required

from application.blueprints import articles as articles_blueprint
from application.blueprints import auth as auth_blueprint
from application.blueprints import inventory as inventory_blueprint
from application.blueprints import items as items_blueprint
from utils import mongo_db, tag, vdo

APP_PATH = os.path.dirname(os.path.abspath(__file__))
TAGS_PATH = os.path.join(APP_PATH, "templates", "tags")

app = Flask(__name__)
app.secret_key = "some_secret"

auth_blueprint.login_manager.init_app(app)
auth_blueprint.bcrypt.init_app(app)
app.register_blueprint(auth_blueprint.blueprint)
app.register_blueprint(articles_blueprint.blueprint)
app.register_blueprint(items_blueprint.blueprint)
app.register_blueprint(inventory_blueprint.blueprint)


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


@app.route("/tag")
@login_required
def get_tags():
    tag_files = [
        f
        for f in os.listdir(TAGS_PATH)
        if os.path.isfile(os.path.join(TAGS_PATH, f)) and "etiquette" in f
    ]
    tag_files = sorted(tag_files)

    return render_template("/tags/tags_list.html", tag_files=tag_files)


@app.route("/<shop>/tag/create", methods=["GET", "POST"])
@login_required
def create_tag(shop):
    if request.method == "GET":
        articles = mongo_db.get_articles()
        return render_template(
            "article_list_glob.html", action="tag", articles=articles, shop=shop
        )

    if request.method == "POST":
        tag_dict = request.form.to_dict()
        tag_list = [
            (mongo_db.get_article_by_id(k).model_dump(), int(v))
            for (k, v) in tag_dict.items()
            if v != ""
        ]
        for article, _ in tag_list:
            article["ratio_category"] = mongo_db.get_type(
                "name", article["type"], "ratio_category"
            )
        tag_beer_list, tag_spirit_list = vdo.format_tag_list(tag_list)

        if tag_beer_list:
            etiquette = tag.PriceTag()
            demonym_dict = mongo_db.get_demonym()
            etiquette.write_beer_tag(tag_beer_list, shop, demonym_dict)

        if tag_spirit_list:
            etiquette = tag.PriceTag()
            etiquette.write_spirit_tag(tag_spirit_list, shop)

        return redirect(url_for("get_tags"))


@app.route("/tag/<tag_file>")
@login_required
def print_tag(tag_file):
    return render_template(f"/tags/{tag_file}")
