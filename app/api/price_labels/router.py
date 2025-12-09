from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import (
    get_current_user,
    get_domain,
    get_settings,
    get_templates,
)
from app.api.price_labels.dtos import PriceLabelRequest
from app.api.utils import url_for_with_query
from app.core.config.settings import Settings
from app.domain.domain import Domain
from app.domain.price_labels.entities import PriceLabelCreate
from app.domain.stores.entities import Store
from app.domain.users.entities import User

router = APIRouter(prefix="/price-labes")


@router.get("/create")
def create_price_labels_view(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    articles = domain.get_articles()
    return templates.TemplateResponse(
        request=request,
        name="article_list_glob.html",
        context={
            "current_user": current_user,
            "articles": articles,
        },
    )


@router.post("/create", dependencies=[Depends(get_current_user)])
def create_price_labels(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    current_store: Store,  # TODO: to refactor
    domain: Annotated[Domain, Depends(get_domain)],
    form_data: Annotated[PriceLabelRequest, Form()],
) -> Response:
    price_labels_create = [
        PriceLabelCreate(article_id=item.article_id, label_count=item.label_count)
        for item in form_data.data
    ]
    domain.create_price_labels(
        settings=settings,
        current_store=current_store,
        price_labels_create=price_labels_create,
    )
    url = url_for_with_query(
        request,
        name="create_price_labels_view",
        query_params={"shop": current_store.slug},
    )
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


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
        name="price_labels/price_labels.html",
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
        name=f"price_labels/temp/{file}",
        context={
            "current_user": current_user,
            "file": file,
        },
    )


@router.delete("/files/delete/{file}", dependencies=[Depends(get_current_user)])
def delete_price_labels_file(
    settings: Annotated[Settings, Depends(get_settings)],
    file: str,
) -> None:
    Path.unlink(settings.app_path.price_labels / file)
