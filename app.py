import json
import os

from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from utils import mongo_db, tactill, tag, vdo
from utils.vdo import calculate_margin, calculate_profit, calculate_recommended_price

APP_PATH = os.path.dirname(os.path.abspath(__file__))
TAGS_PATH = os.path.join(APP_PATH, "templates", "tags")

app = Flask(__name__)
app.secret_key = "some_secret"
app.config["VERIFY_SSL"] = os.environ.get("VERIFY_SSL", "True") == "True"

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)


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
class User(UserMixin):
    def __init__(self, name, username, email, password_hash, shops):
        self.name = name
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.shops = shops

    def get_id(self):
        return self.email

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    user_load = mongo_db.get_user_by_email(user_id)
    return User(
        user_load["name"],
        user_load["username"],
        user_load["email"],
        user_load["password"],
        user_load["shops"],
    )


@app.route("/login", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(
            url_for("get_articles", shop=current_user.shops[0], list_category="beer")
        )

    if request.method == "POST":
        user_db = mongo_db.get_user_by_email(request.form["email"])
        # !!! Ne tient pas compte d'un email qui n'existe pas !!!
        user = User(
            user_db["name"],
            user_db["username"],
            user_db["email"],
            user_db["password"],
            user_db["shops"],
        )
        if user is None or not user.check_password(request.form["password"]):
            flash(
                "Cette combinaison adresse email / mot de passe est invalide.",
                category="error",
            )
            return redirect(url_for("login"))
        login_user(user)

        return redirect(
            url_for("get_articles", shop=current_user.shops[0], list_category="beer")
        )

    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


# =============================================================================
@app.route("/demo")
def demo():
    articles = mongo_db.get_articles_by_list("beer")
    return render_template("demo_list.html", shop="pessac", articles=articles[:100])


# =============================================================================
@app.route("/<shop>/catalog/articles/<list_category>")
@login_required
def get_articles(shop, list_category):
    if request.view_args["shop"] not in current_user.shops:
        abort(401)

    ratio_category = mongo_db.get_type("list_category", list_category, "ratio_category")
    articles = list(mongo_db.get_articles_by_list(list_category))
    shops_margins = mongo_db.get_shops_margins()
    formated_articles = vdo.format_articles_to_list(
        articles, ratio_category, shops_margins, shop
    )

    return render_template(
        "article_list.html",
        shop=shop,
        list_category=list_category,
        articles=formated_articles,
    )


# =============================================================================
@app.route("/catalog/create/<list_category>", methods=["GET", "POST"])
@login_required
def create_article(list_category):
    ratio_category = mongo_db.get_type("list_category", list_category, "ratio_category")

    if request.method == "GET":
        type_list = mongo_db.get_types_by_list([list_category])
        dropdown = mongo_db.get_dropdown(list_category)
        return render_template(
            "article_create.html",
            list_category=list_category,
            ratio_category=ratio_category,
            type_list=type_list,
            **dropdown,
        )

    if request.method == "POST":
        if "cancel" not in request.form.keys():
            request_form = request.form.to_dict(flat=True)
            shops_margins = mongo_db.get_shops_margins()
            formated_article = vdo.format_article_to_db(
                "create",
                {},
                request_form,
                current_user.name,
                shops_margins,
                ratio_category,
            )
            result = mongo_db.create_article(formated_article)

            # -----------------------------------------------------------------
            # Tactill
            tactill_name = vdo.define_tactill_name(formated_article, list_category)
            tactill_icon_text = vdo.define_tactill_icon_text(formated_article["volume"])
            tactill_category = mongo_db.get_type(
                "name", formated_article["type"], "tactill_category"
            )
            tactill_color = vdo.define_tactill_color(
                formated_article["color"], list_category
            )

            for shop in shops_margins:
                api_key = mongo_db.get_tactill_api_key(shop)
                session = tactill.Tactill(api_key, verify=app.config["VERIFY_SSL"])
                res = session.create_article(
                    category=tactill_category,
                    tax_rate=formated_article["tax"],
                    name=tactill_name,
                    full_price=formated_article["shops"][shop]["sell_price"],
                    icon_text=tactill_icon_text,
                    color=tactill_color,
                    barcode=formated_article["barcode"],
                    reference=str(result.inserted_id),
                    in_stock="true",
                )
                app.logger.info(f"Tactill create: {res}")
            # -----------------------------------------------------------------

        return redirect(
            url_for(
                "get_articles", shop=current_user.shops[0], list_category=list_category
            )
        )


# =============================================================================
@app.route("/catalog/<action>/<list_category>/<article_id>", methods=["GET", "POST"])
@login_required
def update_article(action, list_category, article_id):
    if request.method == "GET":
        article = mongo_db.get_article_by_id(article_id)
        ratio_category = mongo_db.get_type(
            "list_category", list_category, "ratio_category"
        )
        type_list = mongo_db.get_types_by_list([list_category])

        formated_article = vdo.format_articles_to_update(article, ratio_category)
        dropdown = mongo_db.get_dropdown(list_category)
        return render_template(
            "article_update.html",
            action=action,
            article=formated_article,
            list_category=list_category,
            ratio_category=ratio_category,
            type_list=type_list,
            **dropdown,
        )

    if request.method == "POST":
        if "cancel" not in request.form:
            article = mongo_db.get_article_by_id(article_id)
            ratio_category = mongo_db.get_type(
                "list_category", list_category, "ratio_category"
            )
            shops_margins = mongo_db.get_shops_margins()

            request_form = request.form.to_dict(flat=True)
            updated_article = vdo.format_article_to_db(
                action,
                article,
                request_form,
                current_user.name,
                shops_margins,
                ratio_category,
            )
            mongo_db.update_article(article_id, updated_article)

            # -----------------------------------------------------------------
            # Tactill
            tactill_name = vdo.define_tactill_name(updated_article, list_category)
            tactill_icon_text = vdo.define_tactill_icon_text(updated_article["volume"])
            tactill_color = vdo.define_tactill_color(
                updated_article["color"], list_category
            )

            for shop in shops_margins:
                api_key = mongo_db.get_tactill_api_key(shop)
                session = tactill.Tactill(api_key, verify=app.config["VERIFY_SSL"])
                res = session.update_article(
                    reference=article_id,
                    name=tactill_name,
                    full_price=updated_article["shops"][shop]["sell_price"],
                    icon_text=tactill_icon_text,
                    color=tactill_color,
                    barcode=updated_article["barcode"],
                )
                app.logger.info(f"Tactill update: {res}")
            # -----------------------------------------------------------------

        if action == "validate":
            return redirect(url_for("check_validation"))

        return redirect(
            url_for(
                "get_articles",
                shop=current_user.shops[0],
                list_category=list_category,
            )
        )


# =============================================================================
@app.route("/catalog/delete/<article_id>")
@login_required
def delete_article(article_id):
    mongo_db.delete_article(article_id)

    # -------------------------------------------------------------------------
    # Tactill
    for shop in mongo_db.get_shop_usernames():
        api_key = mongo_db.get_tactill_api_key(shop)
        session = tactill.Tactill(api_key, verify=app.config["VERIFY_SSL"])
        res = session.delete_article(article_id)
        app.logger.info(f"Tactill delete: {res}")
    # -------------------------------------------------------------------------

    return redirect(request.referrer)


# =============================================================================
@app.route("/catalog/validate")
@login_required
def check_validation():
    articles = list(mongo_db.get_articles_to_validate())
    types_dict = mongo_db.get_types_dict()
    articles_to_validate = vdo.format_articles_to_validate(articles, types_dict)
    return render_template(
        "article_list_glob.html", action="validate", articles=articles_to_validate
    )


@app.route("/catalog/validate/<article_id>")
@login_required
def validate_article(article_id):
    mongo_db.validate_article(article_id)
    return redirect(request.referrer)


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
        dropdown = request.form.to_dict(flat=True)
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
