from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from application.blueprints.auth import Role, admin_required
from application.entities.article import (
    Article,
    ArticleShops,
    ArticleType,
    AugmentedArticle,
    CreateOrUpdateArticle,
    RequestArticle,
)
from application.entities.shop import Shop
from application.use_cases.articles import (
    compute_article_margin,
    compute_recommended_price,
)
from application.use_cases.tactill import TactillManager
from utils import mongo_db

blueprint = Blueprint(name="articles", import_name=__name__, url_prefix="/articles")


@blueprint.get("/<list_category>")
@login_required
def get_articles(list_category: str):
    request_shop = request.args["shop"]
    current_shop = mongo_db.get_shop_by_username(username=request_shop)

    articles = mongo_db.get_articles_by_list(list_category)
    ratio_category = mongo_db.get_ratio_category(list_category)

    augmented_articles = []
    for article in articles:
        recommended_price = compute_recommended_price(
            taxfree_price=article.taxfree_price,
            tax=article.tax,
            shop_margins=current_shop.margins[ratio_category],
            ratio_category=ratio_category,
        )
        margin = compute_article_margin(
            taxfree_price=article.taxfree_price,
            tax=article.tax,
            sell_price=article.shops[current_shop.username].sell_price,
        )

        augmented_article = AugmentedArticle(
            **article.model_dump(by_alias=True),
            recommended_price=recommended_price,
            margin=margin,
        )
        augmented_articles.append(augmented_article)

    return render_template(
        "article_list.html",
        current_shop=current_shop,
        list_category=list_category,
        articles=augmented_articles,
    )


@blueprint.get("/create/<list_category>")
@login_required
def create_article_get(list_category: str):
    ratio_category = mongo_db.get_ratio_category(list_category)
    article_types = mongo_db.get_article_types_by_list(list_category)
    dropdown = mongo_db.get_dropdown(list_category)

    return render_template(
        "article_create.html",
        list_category=list_category,
        ratio_category=ratio_category,
        type_list=[x.name for x in article_types],
        **dropdown,
    )


@blueprint.post("/create/<list_category>")
@login_required
def create_article(list_category: str):
    if "cancel" not in request.form.keys():
        request_form = request.form.to_dict()
        format_request_form(request_form)
        request_article = RequestArticle(**request_form)

        shops = mongo_db.get_shops()
        article_type = mongo_db.get_article_type(request_article.type)
        article_shops = create_article_shops(
            request_form=request_form,
            request_article=request_article,
            shops=shops,
            article_type=article_type,
        )

        validated = current_user.role == Role.ADMIN
        date = datetime.now(timezone.utc)
        article_create = CreateOrUpdateArticle(
            validated=validated,
            created_by=current_user.name,
            created_at=date,
            updated_at=date,
            shops=article_shops,
            **request_article.model_dump(),
        )
        insert_result = mongo_db.create_article(article_create)

        for shop in shops:
            result = TactillManager.create(
                shop=shop,
                article=article_create,
                article_type=article_type,
                article_id=str(insert_result.inserted_id),
            )
            print(result)

    return redirect(
        url_for(
            "articles.get_articles",
            shop=current_user.shops[0],
            list_category=list_category,
        )
    )


@blueprint.get("/update/<article_id>")
@login_required
def update_article_get(article_id: str):
    article = mongo_db.get_article_by_id(article_id)
    article_type = mongo_db.get_article_type(article.type)
    dropdown = mongo_db.get_dropdown(article_type.list_category)

    return render_template(
        "article_update.html",
        article=article,
        list_category=article_type.list_category,
        ratio_category=article_type.ratio_category,
        **dropdown,
    )


@blueprint.post("/update/<article_id>")
@login_required
def update_article(article_id: str):
    article = mongo_db.get_article_by_id(article_id)
    article_type = mongo_db.get_article_type(article.type)

    if "cancel" not in request.form:
        request_form = request.form.to_dict()
        format_request_form(request_form)
        request_article = RequestArticle(**request_form)

        shops = mongo_db.get_shops()
        article_shops = update_article_shops(
            article=article,
            article_type=article_type,
            request_article=request_article,
            request_form=request_form,
            shops=shops,
        )

        validated = True if current_user.role == Role.ADMIN else article.validated
        date = datetime.now(timezone.utc)
        article_update = CreateOrUpdateArticle(
            validated=validated,
            created_by=article.created_by,
            created_at=article.created_at,
            updated_at=date,
            shops=article_shops,
            **request_article.model_dump(),
        )
        mongo_db.update_article(article_id, article_update)

        for shop in shops:
            result = TactillManager.update(
                shop=shop,
                article=article_update,
                article_type=article_type,
                article_id=article_id,
            )
            print(result)

    if _ := request.args.get("validate"):
        return redirect(url_for("articles.validate_articles"))

    return redirect(
        url_for(
            "articles.get_articles",
            shop=current_user.shops[0],
            list_category=article_type.list_category,
        )
    )


@blueprint.get("/delete/<article_id>")
@admin_required
@login_required
def delete_article(article_id: str):
    mongo_db.delete_article(article_id)

    for shop in mongo_db.get_shops():
        result = TactillManager.delete(shop=shop, article_id=article_id)
        print(result)

    return redirect(request.referrer)


@blueprint.get("/validate")
@admin_required
@login_required
def validate_articles():
    articles = mongo_db.get_articles(to_validate=True)
    return render_template("articles_to_validate.html", articles=articles)


@blueprint.get("/validate/<article_id>")
@admin_required
@login_required
def validate_article(article_id):
    mongo_db.validate_article(article_id)
    return redirect(request.referrer)


@blueprint.post("/recommended_prices")
@login_required
def get_recommended_prices():
    ratio_category = request.form["ratio_category"]
    taxfree_price = request.form.get("taxfree_price", default=0, type=float)
    tax = request.form.get("tax", default=0, type=float)

    shops = mongo_db.get_shops()
    recommended_prices = {
        shop.username: compute_recommended_price(
            taxfree_price=taxfree_price,
            tax=tax,
            shop_margins=shop.margins[ratio_category],
            ratio_category=ratio_category,
        )
        for shop in shops
    }
    return jsonify(recommended_prices)


@blueprint.post("/margins")
@login_required
def get_margins():
    taxfree_price = request.form.get("taxfree_price", default=0, type=float)
    tax = request.form.get("tax", default=0, type=float)
    sell_price = request.form.get("sell_price", default=0, type=float)

    article_margin = compute_article_margin(
        taxfree_price=taxfree_price, tax=tax, sell_price=sell_price
    )

    return jsonify(article_margin.model_dump())


def format_request_form(request_form: dict[str, Any]) -> None:
    format_request_name(request_form)
    format_request_deposit(request_form)
    format_request_food_pairing(request_form)


def format_request_name(request_form: dict[str, Any]) -> None:
    request_form["name"] = {
        "name1": request_form.pop("name1", ""),
        "name2": request_form.pop("name2", ""),
    }


def format_request_deposit(request_form: dict[str, Any]) -> None:
    request_form["deposit"] = {
        "unit": request_form.pop("unit", 0),
        "case": request_form.pop("case", 0),
    }


def format_request_food_pairing(request_form: dict[str, Any]) -> None:
    request_form["food_pairing"] = []
    for index in range(6):
        if food_pairing := request_form.pop(f"food_pairing_{index}", None):
            request_form["food_pairing"].append(food_pairing)


def create_article_shops(
    request_form: dict[str, Any],
    request_article: RequestArticle,
    shops: list[Shop],
    article_type: ArticleType,
) -> ArticleShops:
    article_shops = defaultdict(dict)
    for shop in shops:
        sell_price = request_form.get(
            f"sell_price_{shop.username}"
        ) or compute_recommended_price(
            taxfree_price=request_article.taxfree_price,
            tax=request_article.tax,
            shop_margins=shop.margins[article_type.ratio_category],
            ratio_category=article_type.ratio_category,
        )
        article_shops[shop.username]["sell_price"] = sell_price

        bar_price = request_form.get(f"bar_price_{shop.username}", 0)
        article_shops[shop.username]["bar_price"] = bar_price

        article_shops[shop.username]["stock_quantity"] = 0

    return ArticleShops(**article_shops)


def update_article_shops(
    article: Article,
    article_type: ArticleType,
    request_article: RequestArticle,
    request_form: dict[str, Any],
    shops: list[Shop],
) -> ArticleShops:
    price_updated = (
        request_article.buy_price != article.buy_price
        or request_article.excise_duty != article.excise_duty
        or request_article.buy_price != article.social_security_levy
    )

    article_shops = defaultdict(dict)
    for shop in shops:
        article_shops[shop.username]["sell_price"] = update_sell_price(
            article=article,
            article_type=article_type,
            request_article=request_article,
            request_form=request_form,
            shop=shop,
            price_updated=price_updated,
        )
        article_shops[shop.username]["bar_price"] = update_bar_price(
            article=article, request_form=request_form, shop=shop
        )
        article_shops[shop.username]["stock_quantity"] = update_stock_quantity(
            article=article, request_form=request_form, shop=shop
        )
    return ArticleShops(**article_shops)


def update_sell_price(
    article: Article,
    article_type: ArticleType,
    request_article: RequestArticle,
    request_form: dict[str, Any],
    shop: Shop,
    price_updated: bool,
) -> float:
    sell_price = request_form.get(f"sell_price_{shop.username}")

    # sell price is in the request form
    if sell_price is not None:
        return sell_price

    # buy price has been updated, sell price is taken as recommended price
    if price_updated:
        return compute_recommended_price(
            taxfree_price=request_article.taxfree_price,
            tax=article.tax,
            shop_margins=shop.margins[article_type.ratio_category],
            ratio_category=article_type.ratio_category,
        )

    # buy price has not changed, return previous value
    return article.shops[shop.username].sell_price


def update_bar_price(
    article: Article, request_form: dict[str, Any], shop: Shop
) -> float:
    bar_price = request_form.get(f"bar_price_{shop.username}")
    if bar_price is not None:
        return bar_price
    return article.shops[shop.username].bar_price


def update_stock_quantity(
    article: Article, request_form: dict[str, Any], shop: Shop
) -> int:
    stock_quantity = request_form.get(f"stock_quantity_{shop.username}")
    if stock_quantity is not None:
        return stock_quantity
    return article.shops[shop.username].stock_quantity
