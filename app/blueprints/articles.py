import ast
from collections import defaultdict
from typing import Any

from flask import (
    Blueprint,
    Response,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from app.blueprints.auth import admin_required
from app.entities.article import (
    Article,
    ArticleShops,
    ArticleType,
    RequestArticle,
    RequestMargins,
    RequestRecommendedPrices,
)
from app.entities.shop import Shop
from app.use_cases.articles import (
    ArticleManager,
    compute_article_margin,
    compute_recommended_price,
)
from app.worker import (
    create_tactill_articles,
    delete_tactill_articles,
    update_tactill_articles,
)

blueprint = Blueprint(name="articles", import_name=__name__, url_prefix="/articles")


@blueprint.get("/<list_category>")
@login_required
def get_articles(list_category: str) -> str:
    repository = current_app.config["repository_provider"]()

    request_shop = request.args["shop"]
    current_shop = repository.get_shop_by_username(username=request_shop)

    augmented_articles = ArticleManager.list(
        repository=repository, list_category=list_category, current_shop=current_shop
    )

    return render_template(
        "article_list.html",
        current_shop=current_shop,
        list_category=list_category,
        articles=augmented_articles,
    )


@blueprint.get("/create/<list_category>")
@login_required
def create_article_get(list_category: str) -> str:
    repository = current_app.config["repository_provider"]()

    article_types = repository.get_article_types_by_list(list_category)
    ratio_category = article_types[0].ratio_category
    volume_category = article_types[0].volume_category
    items = repository.get_items_dict(volume_category)

    return render_template(
        "article/article.html",
        list_category=list_category,
        ratio_category=ratio_category,
        type_list=[x.name for x in article_types],
        **items,
    )


@blueprint.post("/create/<list_category>")
@login_required
def create_article(list_category: str):
    if "cancel" not in request.form:
        food_pairing = request.form.getlist("food_pairing")
        request_form: dict[str, Any] = request.form.to_dict()
        request_form["food_pairing"] = food_pairing
        format_request_form(request_form)
        request_article = RequestArticle(**request_form)

        repository = current_app.config["repository_provider"]()

        shops = repository.get_shops()
        article_type = repository.get_article_type(request_article.type)
        article_shops = create_article_shops(
            request_form=request_form,
            request_article=request_article,
            shops=shops,
            article_type=article_type,
        )

        inserted_article = ArticleManager.create(
            repository=repository,
            current_user=current_user,
            request_article=request_article,
            article_shops=article_shops,
        )

        create_tactill_articles.delay(inserted_article.id)

    return redirect(
        url_for(
            "articles.get_articles",
            shop=current_user.shops[0],
            list_category=list_category,
        )
    )


@blueprint.get("/update/<article_id>")
@login_required
def update_article_get(article_id: str) -> str:
    repository = current_app.config["repository_provider"]()

    article = repository.get_article_by_id(article_id)
    article_type = repository.get_article_type(article.type)
    items = repository.get_items_dict(article_type.volume_category)

    return render_template(
        "article/article.html",
        article=article,
        list_category=article_type.list_category,
        ratio_category=article_type.ratio_category,
        **items,
    )


@blueprint.post("/update/<article_id>")
@login_required
def update_article(article_id: str):
    repository = current_app.config["repository_provider"]()

    article = repository.get_article_by_id(article_id)
    article_type = repository.get_article_type(article.type)

    if "cancel" not in request.form:
        food_pairing = request.form.getlist("food_pairing")
        request_form: dict[str, Any] = request.form.to_dict()
        request_form["food_pairing"] = food_pairing
        format_request_form(request_form)
        request_article = RequestArticle(**request_form)

        shops = repository.get_shops()
        article_shops = update_article_shops(
            article=article,
            article_type=article_type,
            request_article=request_article,
            request_form=request_form,
            shops=shops,
        )

        updated_article = ArticleManager.update(
            repository=repository,
            current_user=current_user,
            request_article=request_article,
            article_shops=article_shops,
            article=article,
        )

        update_tactill_articles.delay(updated_article.id)

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
    repository = current_app.config["repository_provider"]()
    ArticleManager.delete(repository=repository, article_id=article_id)
    delete_tactill_articles.delay(article_id)
    return redirect(request.referrer)


@blueprint.get("/validate")
@admin_required
@login_required
def validate_articles() -> str:
    repository = current_app.config["repository_provider"]()
    articles = repository.get_articles(to_validate=True)

    return render_template("articles_to_validate.html", articles=articles)


@blueprint.get("/validate/<article_id>")
@admin_required
@login_required
def validate_article(article_id: str):
    repository = current_app.config["repository_provider"]()
    repository.validate_article(article_id)

    return redirect(request.referrer)


@blueprint.post("/recommended_prices")
@login_required
def get_recommended_prices() -> Response:
    data = request.json
    if not data:
        return jsonify({})

    request_data = RequestRecommendedPrices.model_validate(data)

    repository = current_app.config["repository_provider"]()
    shops = repository.get_shops()
    recommended_prices = {
        shop.username: compute_recommended_price(
            taxfree_price=request_data.taxfree_price,
            tax=request_data.tax,
            shop_margins=shop.margins[request_data.ratio_category],
            ratio_category=request_data.ratio_category,
        )
        for shop in shops
    }

    return jsonify(recommended_prices)


@blueprint.post("/margins")
@login_required
def get_margins() -> Response:
    data = request.json
    if not data:
        return jsonify({})

    request_data = RequestMargins.model_validate(data)

    article_margin = compute_article_margin(
        taxfree_price=request_data.taxfree_price,
        tax=request_data.tax,
        sell_price=request_data.sell_price,
    )

    return jsonify(article_margin.model_dump())


def format_request_form(request_form: dict[str, Any]) -> None:
    format_request_name(request_form)
    format_request_volume(request_form)
    format_request_deposit(request_form)


def format_request_name(request_form: dict[str, Any]) -> None:
    request_form["name"] = {
        "name1": request_form.pop("name1", ""),
        "name2": request_form.pop("name2", ""),
    }


def format_request_volume(request_form: dict[str, Any]) -> None:
    request_volume = request_form.pop("volume", None)
    if request_volume is not None:
        volume = ast.literal_eval(request_volume)
        request_form["volume"] = {"value": volume["value"], "unit": volume["unit"]}
    else:
        request_form["volume"] = None


def format_request_deposit(request_form: dict[str, Any]) -> None:
    request_form["deposit"] = {
        "unit": request_form.pop("unit", 0),
        "case": request_form.pop("case", 0),
    }


def create_article_shops(
    request_form: dict[str, Any],
    request_article: RequestArticle,
    shops: list[Shop],
    article_type: ArticleType,
) -> ArticleShops:
    article_shops: defaultdict[str, dict[str, Any]] = defaultdict(dict)
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

    article_shops: defaultdict[str, dict[str, Any]] = defaultdict(dict)
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
        article_shops[shop.username]["stock_quantity"] = article.shops[
            shop.username
        ].stock_quantity

    return ArticleShops.model_validate(article_shops)


def update_sell_price(
    article: Article,
    article_type: ArticleType,
    request_article: RequestArticle,
    request_form: dict[str, Any],
    shop: Shop,
    price_updated: bool,
) -> float:
    sell_price: float | None = request_form.get(f"sell_price_{shop.username}")

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
    bar_price: float | None = request_form.get(f"bar_price_{shop.username}")
    if bar_price is not None:
        return bar_price
    return article.shops[shop.username].bar_price
