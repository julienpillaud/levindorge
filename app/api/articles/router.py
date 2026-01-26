from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.params import Query
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from pydantic import PositiveInt

from app.api.articles.dtos import ArticleDTO, MarginsRequestDTO, PriceRequestDTO
from app.api.dependencies import get_current_user, get_domain, get_templates
from app.domain.articles.entities import ArticleCreateOrUpdate, ArticleMargins
from app.domain.articles.utils import compute_article_margins, compute_recommended_price
from app.domain.commons.category_groups import CATEGORY_GROUPS_MAP, CategoryGroupName
from app.domain.domain import Domain
from app.domain.entities import DEFAULT_PAGINATION_SIZE, EntityId

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("", dependencies=[Depends(get_current_user)])
def get_articles(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    search: str | None = None,
    page: PositiveInt = 1,
    limit: PositiveInt = DEFAULT_PAGINATION_SIZE,
) -> Response:
    result = domain.get_articles(search=search, page=page, limit=limit)
    return templates.TemplateResponse(
        request=request,
        name="articles/articles.html",
        context={"result": result},
    )


@router.get("/ids", dependencies=[Depends(get_current_user)])
def get_articles_by_ids(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    article_ids: Annotated[list[EntityId], Query()],
) -> Response:
    result = domain.get_articles_by_ids(article_ids)
    return templates.TemplateResponse(
        request=request,
        name="articles/articles.html",
        context={"result": result},
    )


@router.get("/create/{category_group_name}", dependencies=[Depends(get_current_user)])
def create_article_view(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    category_group_name: CategoryGroupName,
) -> Response:
    stores = domain.get_stores()
    categories = domain.get_categories(category_group=category_group_name)
    category_group = CATEGORY_GROUPS_MAP[category_group_name]
    data = domain.get_view_data(category_group=category_group)
    return templates.TemplateResponse(
        request=request,
        name="articles/_article.html",
        context={
            "stores": stores.items,
            "article": None,
            "categories": categories.items,
            "category_group": category_group,
            "data": data,
        },
    )


@router.post("/create", dependencies=[Depends(get_current_user)])
def create_article(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    form_data: Annotated[ArticleDTO, Form()],
) -> Response:
    article_create = ArticleCreateOrUpdate(**form_data.model_dump())
    article = domain.create_article(data=article_create)
    return templates.TemplateResponse(
        request=request,
        name="articles/_article_row.html",
        context={"article": article},
    )


@router.get("/update/{article_id}", dependencies=[Depends(get_current_user)])
def update_article_view(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    article_id: EntityId,
) -> Response:
    stores = domain.get_stores()
    article = domain.get_article(article_id=article_id)
    category = domain.get_category_by_name(article.category)
    category_group = CATEGORY_GROUPS_MAP[category.category_group]
    data = domain.get_view_data(category_group=category_group)
    return templates.TemplateResponse(
        request=request,
        name="articles/_article.html",
        context={
            "stores": stores.items,
            "article": article,
            "category_group": category_group,
            "data": data,
        },
    )


@router.post("/update/{article_id}", dependencies=[Depends(get_current_user)])
def update_article(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    form_data: Annotated[ArticleDTO, Form()],
    article_id: EntityId,
) -> Response:
    article_update = ArticleCreateOrUpdate(**form_data.model_dump())
    article = domain.update_article(article_id=article_id, data=article_update)
    return templates.TemplateResponse(
        request=request,
        name="articles/_article_row.html",
        context={"article": article},
    )


@router.delete("/{article_id}", dependencies=[Depends(get_current_user)])
def delete_article(
    domain: Annotated[Domain, Depends(get_domain)],
    article_id: EntityId,
) -> None:
    domain.delete_article(article_id=article_id)


@router.post("/recommended_prices")
async def recommended_prices(
    domain: Annotated[Domain, Depends(get_domain)],
    data: PriceRequestDTO,
) -> dict[str, Decimal]:
    stores = domain.get_stores()
    return {
        store.slug: compute_recommended_price(
            total_cost=data.total_cost,
            vat_rate=data.vat_rate,
            pricing_group=data.pricing_group,
            pricing_config=store.pricing_configs[data.pricing_group],
        )
        for store in stores.items
    }


@router.post("/margins")
async def margins(data: MarginsRequestDTO) -> ArticleMargins:
    return compute_article_margins(
        total_cost=data.total_cost,
        vat_rate=data.vat_rate,
        gross_price=data.gross_price,
    )
