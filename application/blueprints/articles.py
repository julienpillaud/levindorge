from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from utils import mongo_db, tactill, vdo

blueprint = Blueprint(name="articles", import_name=__name__, url_prefix="/articles")


@blueprint.get("/<list_category>")
@login_required
def get_articles(list_category: str):
    shop = request.args["shop"]
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


@blueprint.get("/create/<list_category>")
@login_required
def create_article_get(list_category: str):
    ratio_category = mongo_db.get_type("list_category", list_category, "ratio_category")
    type_list = mongo_db.get_types_by_list([list_category])
    dropdown = mongo_db.get_dropdown(list_category)

    return render_template(
        "article_create.html",
        list_category=list_category,
        ratio_category=ratio_category,
        type_list=type_list,
        **dropdown,
    )


@blueprint.post("/create/<list_category>")
@login_required
def create_article(list_category: str):
    if "cancel" not in request.form.keys():
        ratio_category = mongo_db.get_type(
            "list_category", list_category, "ratio_category"
        )
        request_form = request.form.to_dict()
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
            session = tactill.Tactill(api_key)
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
            print(res)

    return redirect(
        url_for(
            "articles.get_articles",
            shop=current_user.shops[0],
            list_category=list_category,
        )
    )


@blueprint.get("/update/<article_id>")
@login_required
def update_article_get(article_id):
    article = mongo_db.get_article_by_id(article_id)

    list_category = mongo_db.get_type("name", article["type"], "list_category")
    ratio_category = mongo_db.get_type("list_category", list_category, "ratio_category")
    type_list = mongo_db.get_types_by_list([list_category])

    formated_article = vdo.format_articles_to_update(article, ratio_category)
    dropdown = mongo_db.get_dropdown(list_category)
    return render_template(
        "article_update.html",
        article=formated_article,
        list_category=list_category,
        ratio_category=ratio_category,
        type_list=type_list,
        **dropdown,
    )


@blueprint.post("/update/<article_id>")
@login_required
def update_article(article_id):
    article = mongo_db.get_article_by_id(article_id)
    list_category = mongo_db.get_type("name", article["type"], "list_category")

    if "cancel" not in request.form:
        ratio_category = mongo_db.get_type(
            "list_category", list_category, "ratio_category"
        )
        shops_margins = mongo_db.get_shops_margins()

        request_form = request.form.to_dict()
        updated_article = vdo.format_article_to_db(
            "update",
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
            session = tactill.Tactill(api_key)
            session.update_article(
                reference=article_id,
                name=tactill_name,
                full_price=updated_article["shops"][shop]["sell_price"],
                icon_text=tactill_icon_text,
                color=tactill_color,
                barcode=updated_article["barcode"],
            )
        # -----------------------------------------------------------------

    return redirect(
        url_for(
            "articles.get_articles",
            shop=current_user.shops[0],
            list_category=list_category,
        )
    )


@blueprint.get("/delete/<article_id>")
@login_required
def delete_article(article_id: str):
    mongo_db.delete_article(article_id)

    for shop in mongo_db.get_shop_usernames():
        api_key = mongo_db.get_tactill_api_key(shop)
        session = tactill.Tactill(api_key)
        session.delete_article(article_id)

    return redirect(request.referrer)
