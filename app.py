import json
import os

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from application.blueprints import articles, auth
from utils import mongo_db, tag, vdo
from utils.vdo import calculate_margin, calculate_profit, calculate_recommended_price

APP_PATH = os.path.dirname(os.path.abspath(__file__))
TAGS_PATH = os.path.join(APP_PATH, "templates", "tags")

app = Flask(__name__)
app.secret_key = "some_secret"

auth.login_manager.init_app(app)
auth.bcrypt.init_app(app)
app.register_blueprint(auth.blueprint)
app.register_blueprint(articles.blueprint)


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
@app.route("/catalog/taxfree_price", methods=["POST"])
@login_required
def get_taxfree_price():
    """Calculate taxfree price"""
    buy_price = request.form.get("buy_price", default=0, type=float)
    excise_duty = request.form.get("excise_duty", default=0, type=float)
    social_security_levy = request.form.get(
        "social_security_levy", default=0, type=float
    )
    taxfree_price = round(buy_price + excise_duty + social_security_levy, 4)

    return jsonify({"taxfree_price": taxfree_price})


@app.route("/catalog/recommended_prices", methods=["POST"])
@login_required
def get_recommended_prices():
    """Get recommended price for each shop"""
    ratio_category = request.form["ratio_category"]
    taxfree_price = request.form.get("taxfree_price", default=0, type=float)
    tax = request.form.get("tax", default=0, type=float)

    recommended_prices = {}
    shops = mongo_db.get_shops()
    for shop in shops:
        margins = shop["margins"][ratio_category]
        recommended_prices[shop["username"]] = calculate_recommended_price(
            taxfree_price, tax, ratio_category, margins
        )

    return jsonify(recommended_prices)


@app.route("/catalog/margins", methods=["POST"])
@login_required
def get_margins():
    """Get profits and margins for each shop managed by current user"""
    taxfree_price = request.form.get("taxfree_price", default=0, type=float)
    tax = request.form.get("tax", default=0, type=float)
    sell_prices = json.loads(request.form.get("sell_prices"))

    profits = {}
    margins = {}
    for shop in current_user.shops:
        sell_price = sell_prices[f"sell_price_{shop}"]
        sell_price = float(sell_price) if sell_price else 0
        article_profit = calculate_profit(taxfree_price, tax, sell_price)
        profits[shop] = round(article_profit, 2)
        article_margin = calculate_margin(tax, sell_price, article_profit)
        margins[shop] = round(article_margin)

    return jsonify({"profits": profits, "margins": margins})


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
        articles = list(mongo_db.get_articles())
        types_dict = mongo_db.get_types_dict()
        articles_tag = vdo.format_articles_to_validate(articles, types_dict)
        return render_template(
            "article_list_glob.html", action="tag", articles=articles_tag, shop=shop
        )

    if request.method == "POST":
        tag_dict = request.form.to_dict(flat=True)
        tag_list = [
            (mongo_db.get_article_by_id(k), int(v))
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
        mongo_db.get_articles_by_filter(
            {"type": {"$in": ["Bière", "Cidre"]}, "deposit.unit": {"$ne": 0}}
        )
    )
    beer2 = list(
        mongo_db.get_articles_by_filter(
            {"type": {"$in": ["Bière", "Cidre"]}, "deposit.unit": {"$eq": 0}}
        )
    )
    keg = list(mongo_db.get_articles_by_filter({"type": {"$in": ["Fût", "Mini-fût"]}}))

    spirit_types = mongo_db.get_types_by_list(["rhum", "whisky", "arranged", "spirit"])
    spirit = list(mongo_db.get_articles_by_filter({"type": {"$in": spirit_types}}))

    wine_types = mongo_db.get_types_by_list(
        ["wine", "fortified_wine", "sparkling_wine"]
    )
    wine = list(mongo_db.get_articles_by_filter({"type": {"$in": wine_types}}))

    bib = list(mongo_db.get_articles_by_filter({"type": {"$in": ["BIB"]}}))
    box = list(mongo_db.get_articles_by_filter({"type": {"$in": ["Coffret"]}}))
    misc = list(
        mongo_db.get_articles_by_filter(
            {"type": {"$in": ["Accessoire", "Emballage", "BSA"]}}
        )
    )
    food = list(mongo_db.get_articles_by_filter({"type": {"$in": ["Alimentation"]}}))

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

    types_dict = mongo_db.get_types_dict()
    articles_inventory = {}
    for name, articles in articles_list.items():
        articles_inventory[name] = vdo.format_articles_to_validate(articles, types_dict)

    return render_template("inventory.html", articles_inventory=articles_inventory)
