import json
from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from fastapi.datastructures import URL
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_domain
from app.app.articles.dtos import ArticleDTO, MarginsRequestDTO, PriceRequestDTO
from app.app.auth.dependencies import get_current_user
from app.app.dependencies import get_templates
from app.domain.articles.entities import ArticleCreateOrUpdate, ArticleMargins
from app.domain.articles.utils import compute_article_margins, compute_recommended_price
from app.domain.commons.entities import DisplayGroup
from app.domain.domain import Domain
from app.domain.users.entities import User

router = APIRouter(prefix="/articles")


@router.get("/{display_group}")
def get_articles_view(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    display_group: str,
) -> Response:
    category_group = domain.get_category_group(slug=display_group)
    result = domain.get_articles_by_display_group(display_group=display_group)
    articles = result.items
    return templates.TemplateResponse(
        request=request,
        name="articles/articles.html",
        context={
            "current_user": current_user,
            "current_shop": current_user.shops[0],
            "category_group": category_group,
            "articles": articles,
            "articles_mapping": json.dumps(
                {
                    article.id: {
                        shop: shop_data.model_dump()
                        for shop, shop_data in article.shops.items()
                    }
                    for article in articles
                }
            ),
            "display_group": display_group,
        },
    )


@router.get("/create/{display_group}")
def create_article_view(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    display_group: DisplayGroup,
) -> Response:
    view_data = domain.get_view_data(display_group=display_group)
    return templates.TemplateResponse(
        request=request,
        name="articles/article.html",
        context={
            "current_user": current_user,
            "list_category": display_group,
            "ratio_category": view_data.pricing_group,
            "type_list": view_data.article_type_names,
            **view_data.items,
        },
    )


@router.post("/create/{display_group}")
def create_article(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    form_data: Annotated[ArticleDTO, Form()],
    display_group: DisplayGroup,
) -> Response:
    article_create = ArticleCreateOrUpdate(**form_data.model_dump())
    domain.create_article(current_user=current_user, data=article_create)
    return RedirectResponse(
        url=request.url_for("get_articles_view", display_group=display_group),
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/update/{article_id}")
def update_article_view(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    article_id: str,
) -> Response:
    article = domain.get_article(article_id=article_id)
    view_data = domain.get_view_data(name=article.type)
    return templates.TemplateResponse(
        request=request,
        name="articles/article.html",
        context={
            "current_user": current_user,
            "list_category": view_data.display_group,
            "ratio_category": view_data.pricing_group,
            "article": article,
            **view_data.items,
        },
    )


@router.post("/update/{article_id}")
def update_article(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    form_data: Annotated[ArticleDTO, Form()],
    article_id: str,
) -> Response:
    article_update = ArticleCreateOrUpdate(**form_data.model_dump())
    article = domain.update_article(
        current_user=current_user,
        article_id=article_id,
        data=article_update,
    )
    article_type = domain.get_article_type(name=article.type)
    return RedirectResponse(
        url=request.url_for(
            "get_articles_view",
            display_group=article_type.display_group,
        ),
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/delete/{article_id}")
def delete_article(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    article_id: str,
) -> Response:
    domain.delete_article(current_user=current_user, article_id=article_id)
    display_group = URL(request.headers["referer"]).path.split("/")[-1]
    return RedirectResponse(
        url=request.url_for("get_articles_view", display_group=display_group),
        status_code=status.HTTP_302_FOUND,
    )


@router.post("/recommended_prices")
async def recommended_prices(
    current_user: Annotated[User, Depends(get_current_user)],
    data: PriceRequestDTO,
) -> dict[str, float]:
    return {
        shop.username: compute_recommended_price(
            net_price=data.taxfree_price,
            tax_rate=data.tax,
            shop_margins=shop.margins[data.ratio_category],
            pricing_group=data.ratio_category,
        )
        for shop in current_user.shops
    }


@router.post("/margins", dependencies=[Depends(get_current_user)])
async def margins(data: MarginsRequestDTO) -> ArticleMargins:
    return compute_article_margins(
        net_price=data.taxfree_price,
        tax_rate=data.tax,
        gross_price=data.sell_price,
    )
