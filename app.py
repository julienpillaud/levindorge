import os

from flask import Flask, redirect, render_template, request, url_for
from flask_login import login_required

from application.blueprints import articles as articles_blueprint
from application.blueprints import auth as auth_blueprint
from utils import mongo_db, tag, vdo

APP_PATH = os.path.dirname(os.path.abspath(__file__))
TAGS_PATH = os.path.join(APP_PATH, "templates", "tags")

app = Flask(__name__)
app.secret_key = "some_secret"

auth_blueprint.login_manager.init_app(app)
auth_blueprint.bcrypt.init_app(app)
app.register_blueprint(auth_blueprint.blueprint)
app.register_blueprint(articles_blueprint.blueprint)


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


# =============================================================================
@app.route("/demo")
def demo():
    articles = mongo_db.get_articles_by_list("beer")
    return render_template("demo_list.html", shop="pessac", articles=articles[:100])


# =============================================================================
@app.route("/dropdown/<dropdown_category>/create", methods=["GET", "POST"])
@login_required
def get_dropdown(dropdown_category):
    if request.method == "GET":
        return render_template(
            "dropdown_list.html",
            dropdown_name=mongo_db.DROPDOWN_DICT[dropdown_category]["name"],
            dropdown_category=dropdown_category,
            dropdown_list=mongo_db.get_dropdown_by_category(dropdown_category),
        )

    if request.method == "POST":
        dropdown = request.form.to_dict()
        mongo_db.create_dropdown(dropdown_category, dropdown)
        return redirect(url_for("get_dropdown", dropdown_category=dropdown_category))


@app.route("/dropdown/<dropdown_category>/delete/<dropdown_id>")
@login_required
def delete_dropdown(dropdown_category, dropdown_id):
    mongo_db.delete_dropdown(dropdown_category, dropdown_id)
    return redirect(request.referrer)


# =============================================================================
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


# =============================================================================
@app.route("/inventory")
@login_required
def inventory():
    beer1 = list(
        mongo_db.get_articles(
            {"type": {"$in": ["Bière", "Cidre"]}, "deposit.unit": {"$ne": 0}}
        )
    )
    beer2 = list(
        mongo_db.get_articles(
            {"type": {"$in": ["Bière", "Cidre"]}, "deposit.unit": {"$eq": 0}}
        )
    )
    keg = list(mongo_db.get_articles({"type": {"$in": ["Fût", "Mini-fût"]}}))

    spirit_types = mongo_db.get_types_by_list(["rhum", "whisky", "arranged", "spirit"])
    spirit = list(mongo_db.get_articles({"type": {"$in": spirit_types}}))

    wine_types = mongo_db.get_types_by_list(
        ["wine", "fortified_wine", "sparkling_wine"]
    )
    wine = list(mongo_db.get_articles({"type": {"$in": wine_types}}))

    bib = list(mongo_db.get_articles({"type": {"$in": ["BIB"]}}))
    box = list(mongo_db.get_articles({"type": {"$in": ["Coffret"]}}))
    misc = list(
        mongo_db.get_articles({"type": {"$in": ["Accessoire", "Emballage", "BSA"]}})
    )
    food = list(mongo_db.get_articles({"type": {"$in": ["Alimentation"]}}))

    articles_list = {
        "Bières C": beer1,
        "Bières NC": beer2,
        "Fûts": keg,
        "Spiritieux": spirit,
        "Vins": wine,
        "BIB": bib,
        "Coffrets": box,
        "Divers": misc,
        "Alimentation": food,
    }

    return render_template("inventory.html", articles_inventory=articles_list)
