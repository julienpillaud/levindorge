from typing import Annotated, Literal

from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import (
    get_current_user,
    get_domain,
    get_settings,
    get_templates,
)
from app.api.price_labels.dtos import PriceLabelRequest
from app.core.config.settings import Settings
from app.domain.domain import Domain
from app.domain.price_labels.entities import PriceLabelCreate
from app.domain.types import EntityId

router = APIRouter(prefix="/price-labels", tags=["Price Labels"])


@router.post("", dependencies=[Depends(get_current_user)])
def create_price_labels(
    settings: Annotated[Settings, Depends(get_settings)],
    domain: Annotated[Domain, Depends(get_domain)],
    price_labels_request: PriceLabelRequest,
) -> Response:
    price_labels_create = [
        PriceLabelCreate(
            article_id=item.article_id,
            label_count=item.label_count,
        )
        for item in price_labels_request.data
    ]
    domain.create_price_labels(
        settings=settings,
        store_slug=price_labels_request.store_slug,
        price_labels_create=price_labels_create,
    )
    return JSONResponse(content={}, status_code=status.HTTP_201_CREATED)


@router.get("", dependencies=[Depends(get_current_user)])
def get_price_labels(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    price_labels = domain.get_price_labels()
    return templates.TemplateResponse(
        request=request,
        name="price-labels/price-labels.html",
        context={"price_labels": price_labels},
    )


@router.get(
    "/sheet/{price_labels_type}/{price_labels_id}",
    dependencies=[Depends(get_current_user)],
)
def get_price_labels_sheet(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    price_labels_type: Literal["large", "small"],
    price_labels_id: EntityId,
) -> Response:
    price_labels = domain.get_price_labels_sheet(price_labels_id=price_labels_id)
    return templates.TemplateResponse(
        request=request,
        name=f"price-labels/base-{price_labels_type}.html",
        context={"content": price_labels.content},
    )


@router.get("/delete/{price_labels_id}", dependencies=[Depends(get_current_user)])
def delete_price_labels(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    price_labels_id: EntityId,
) -> Response:
    domain.delete_price_labels(price_labels_id=price_labels_id)
    return RedirectResponse(url=request.url_for("get_price_labels"))
