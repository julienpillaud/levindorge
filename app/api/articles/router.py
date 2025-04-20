import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from fastapi.datastructures import URL
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response

from app.api.articles.dtos import ArticleDTO, MarginsRequestDTO, PriceRequestDTO
from app.api.auth.dependencies import get_current_shop, get_current_user
from app.api.dependencies import get_domain
from app.api.templates import templates
from app.api.utils import url_for_with_query
from app.domain.articles.entities import ArticleCreateOrUpdate, ArticleMargin
from app.domain.articles.utils import compute_article_margins, compute_recommended_price
from app.domain.domain import Domain
from app.domain.shops.entities import Shop
from app.domain.users.entities import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/articles", tags=["articles"], include_in_schema=False)


@router.get("/{list_category}")
async def get_articles_view(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    current_shop: Annotated[Shop, Depends(get_current_shop)],
    domain: Annotated[Domain, Depends(get_domain)],
    list_category: str,
) -> Response:
    articles = domain.get_articles(
        current_shop=current_shop,
        list_category=list_category,
    )

    return templates.TemplateResponse(
        request=request,
        name="article_list.html",
        context={
            "current_user": current_user,
            "current_shop": current_shop,
            "articles": articles,
            "list_category": list_category,
        },
    )


@router.get("/create/{list_category}")
def create_article_view(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    list_category: str,
) -> Response:
    type_infos = domain.get_type_infos(list_category=list_category)
    ratio_category = type_infos[0].ratio_category
    volume_category = type_infos[0].volume_category
    template_context = domain.get_template_context(volume_category=volume_category)

    return templates.TemplateResponse(
        request=request,
        name="article/article.html",
        context={
            "current_user": current_user,
            "list_category": list_category,
            "ratio_category": ratio_category,
            "article_types": [type_info.name for type_info in type_infos],
            **template_context,
        },
    )


@router.post("/create/{list_category}")
async def create_article(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    data: Annotated[ArticleDTO, Form()],
):
    article_create = ArticleCreateOrUpdate.model_validate(data.model_dump())
    article = domain.create_article(
        current_user=current_user,
        data=article_create,
    )

    url = url_for_with_query(
        request,
        name="get_articles_view",
        list_category=article.type_infos.list_category,
        query_params={"shop": current_user.shops[0].username},
    )
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@router.get("/update/{article_id}")
async def update_article_view(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    article_id: str,
) -> Response:
    article = domain.get_article(article_id=article_id)
    template_context = domain.get_template_context(
        volume_category=article.type_infos.volume_category
    )

    return templates.TemplateResponse(
        request=request,
        name="article/article.html",
        context={
            "current_user": current_user,
            "list_category": article.type_infos.list_category,
            "ratio_category": article.type_infos.ratio_category,
            "article": article,
            **template_context,
        },
    )


@router.post("/update/{article_id}")
def update_article(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    data: Annotated[ArticleDTO, Form()],
    article_id: str,
):
    article_update = ArticleCreateOrUpdate.model_validate(data.model_dump())
    article = domain.update_article(
        current_user=current_user,
        article_id=article_id,
        data=article_update,
    )

    url = url_for_with_query(
        request,
        name="get_articles_view",
        list_category=article.type_infos.list_category,
        query_params={"shop": current_user.shops[0].username},
    )
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@router.get("/delete/{article_id}")
async def delete_article(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    article_id: str,
) -> Response:
    domain.delete_article(article_id=article_id)

    url = url_for_with_query(
        request,
        name="get_articles_view",
        list_category=URL(request.headers["referer"]).path.split("/")[-1],
        query_params={"shop": current_user.shops[0].username},
    )
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@router.post("/recommended_prices")
async def recommended_prices(
    data: PriceRequestDTO,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return {
        shop.username: compute_recommended_price(
            ratio_category=data.ratio_category,
            taxfree_price=data.taxfree_price,
            tax=data.tax,
            shop=shop,
        )
        for shop in current_user.shops
    }


@router.post("/margins", dependencies=[Depends(get_current_user)])
async def margins(data: MarginsRequestDTO) -> ArticleMargin:
    return compute_article_margins(
        taxfree_price=data.taxfree_price,
        tax=data.tax,
        sell_price=data.sell_price,
    )
