from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_domain
from app.app.auth.dependencies import get_current_user
from app.app.dependencies import get_templates
from app.domain.domain import Domain
from app.domain.items.entities import ItemType
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
    items = domain.get_volumes()
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
    items = domain.get_deposits()
    return templates.TemplateResponse(
        request=request,
        name="items/deposits.html",
        context={
            "current_user": current_user,
            "deposits": items,
        },
    )


@router.get("/{item_type}")
def get_items_view(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    item_type: ItemType,
) -> Response:
    title = ITEMS_TITLE_MAPPING.get(item_type)
    items = domain.get_items(item_type=item_type)
    return templates.TemplateResponse(
        request=request,
        name="items/item_list.html",
        context={
            "current_user": current_user,
            "title": title,
            "category": item_type,
            "items": items,
        },
    )


@router.get("/volumes/{volume_id}/delete")
def delete_volume(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    volume_id: str,
) -> Response:
    domain.delete_volume(volume_id=volume_id)
    return RedirectResponse(
        url=request.url_for("get_volumes_view"),
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/deposits/{deposit_id}/delete")
def delete_deposit(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    deposit_id: str,
) -> Response:
    domain.delete_deposit(deposit_id=deposit_id)
    return RedirectResponse(
        url=request.url_for("get_deposits_view"),
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/{item_type}/{item_id}/delete")
def delete_item(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    item_type: ItemType,
    item_id: str,
) -> Response:
    domain.delete_item(item_type=item_type, item_id=item_id)
    return RedirectResponse(
        url=request.url_for("get_items_view", item_type=item_type),
        status_code=status.HTTP_302_FOUND,
    )
