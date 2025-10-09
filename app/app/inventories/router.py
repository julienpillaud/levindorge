from typing import Annotated

from cleanstack.exceptions import BadRequestError
from fastapi import APIRouter, Depends, Form, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_domain
from app.app.auth.dependencies import get_current_user
from app.app.dependencies import get_templates
from app.domain.domain import Domain
from app.domain.shops.entities import Shop
from app.domain.users.entities import User

router = APIRouter(prefix="/inventories")


def get_shop_from_form(
    current_user: Annotated[User, Depends(get_current_user)],
    shop: Annotated[str, Form()],
) -> Shop:
    for user_shop in current_user.shops:
        if shop == user_shop.username:
            return user_shop
    raise BadRequestError("Invalid shop")


@router.get("")
def get_inventories_view(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    inventories = domain.get_inventories()
    return templates.TemplateResponse(
        request=request,
        name="inventories/inventory_list.html",
        context={
            "current_user": current_user,
            "inventories": inventories,
        },
    )


@router.post("", dependencies=[Depends(get_current_user)])
def create_inventory(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    shop: Annotated[Shop, Depends(get_shop_from_form)],
) -> Response:
    domain.create_inventory(shop=shop)
    return RedirectResponse(
        url=request.url_for("get_inventories_view"),
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/{inventory_id}")
def get_inventory_view(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    inventory_id: str,
) -> Response:
    inventory = domain.get_inventory(inventory_id=inventory_id)
    return templates.TemplateResponse(
        request=request,
        name="inventories/inventory.html",
        context={
            "current_user": current_user,
            "inventory": inventory,
        },
    )


@router.get("/{inventory_id}/delete", dependencies=[Depends(get_current_user)])
def delete_inventory(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    inventory_id: str,
) -> Response:
    domain.delete_inventory(inventory_id=inventory_id)
    return RedirectResponse(
        url=request.url_for("get_inventories_view"),
        status_code=status.HTTP_302_FOUND,
    )


@router.post("/stocks/reset", dependencies=[Depends(get_current_user)])
def reset_pos_stocks(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    shop: Annotated[Shop, Depends(get_shop_from_form)],
    category: Annotated[str, Form()],
) -> Response:
    domain.reset_pos_stocks(shop=shop, category=category)
    return RedirectResponse(
        url=request.url_for("get_inventories_view"),
        status_code=status.HTTP_302_FOUND,
    )
