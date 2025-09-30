from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_domain
from app.app.auth.dependencies import get_current_user
from app.app.dependencies import get_templates
from app.domain.domain import Domain
from app.domain.users.entities import User

router = APIRouter(prefix="/items", tags=["Items"])

ITEMS_TITLE_MAPPING = {
    "breweries": "Brasserie",
    "distilleries": "Distillerie",
    "distributors": "Fournisseur",
    "countries": "Pays",
    "regions": "Région",
}


@router.get("/volumes")
def get_volumes_view(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    items = domain.get_items(name="volumes")
    return templates.TemplateResponse(
        request=request,
        name="items/volumes.html",
        context={
            "current_user": current_user,
            "volumes": items,
        },
    )


@router.get("/deposits")
def get_deposits_view(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    items = domain.get_items(name="deposits")
    return templates.TemplateResponse(
        request=request,
        name="items/deposits.html",
        context={
            "current_user": current_user,
            "deposits": items,
        },
    )


@router.get("/{name}")
def get_items_view(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    name: str,
) -> Response:
    title = ITEMS_TITLE_MAPPING.get(name)
    items = domain.get_items(name=name)
    return templates.TemplateResponse(
        request=request,
        name="items/item_list.html",
        context={
            "current_user": current_user,
            "title": title,
            "category": name,
            "items": items,
        },
    )


@router.get("/{name}/{item_id}")
def delete_item() -> None:
    pass
