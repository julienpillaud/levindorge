from pathlib import Path
from typing import Annotated

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
from app.domain.users.entities import User

router = APIRouter(prefix="/price-labels", tags=["Price Labels"])


@router.post("/create", dependencies=[Depends(get_current_user)])
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


@router.get("/files")
def get_price_labels_files(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    files = domain.get_price_labels_files(settings=settings)
    return templates.TemplateResponse(
        request=request,
        name="price-labels/price-labels.html",
        context={
            "current_user": current_user,
            "files": files,
        },
    )


@router.get("/files/{file}")
def get_price_labels_file(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    file: str,
) -> Response:
    return templates.TemplateResponse(
        request=request,
        name=f"price-labels-files/{file}",
        context={
            "current_user": current_user,
            "file": file,
        },
    )


@router.get("/files/delete/{file}", dependencies=[Depends(get_current_user)])
def delete_price_labels_file(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    file: str,
) -> Response:
    Path.unlink(settings.app_path.price_labels / file)
    return RedirectResponse(url=request.url_for("get_price_labels_files"))
