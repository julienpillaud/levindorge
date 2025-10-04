from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_domain
from app.app.auth.dependencies import get_current_user
from app.app.dependencies import get_templates
from app.domain.domain import Domain
from app.domain.items.entities import ItemCreate, ItemType
from app.domain.users.entities import User

router = APIRouter(prefix="/items")

ITEMS_TITLE_MAPPING = {
    "breweries": "Brasserie",
    "distilleries": "Distillerie",
    "distributors": "Fournisseur",
    "countries": "Pays",
    "regions": "Région",
}


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


@router.post("/{item_type}", dependencies=[Depends(get_current_user)])
def create_item(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    form_data: Annotated[ItemCreate, Form()],
    item_type: ItemType,
) -> Response:
    domain.create_item(item_type=item_type, item_create=form_data)
    return RedirectResponse(
        url=request.url_for("get_items_view", item_type=item_type),
        status_code=status.HTTP_302_FOUND,
    )


@router.get(
    "/{item_type}/{item_id}/delete",
    dependencies=[Depends(get_current_user)],
)
def delete_item(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    item_type: ItemType,
    item_id: str,
) -> Response:
    domain.delete_item(item_type=item_type, item_id=item_id)
    return RedirectResponse(
        url=request.url_for("get_items_view", item_type=item_type),
        status_code=status.HTTP_302_FOUND,
    )
