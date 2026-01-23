from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_current_user, get_domain, get_templates
from app.domain.domain import Domain
from app.domain.entities import EntityId
from app.domain.stores.entities import Store

router = APIRouter(prefix="/inventories", tags=["Inventories"])


@router.get("", dependencies=[Depends(get_current_user)])
def get_inventories(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    inventories = domain.get_inventories()
    return templates.TemplateResponse(
        request=request,
        name="inventories/inventories.html",
        context={"result": inventories},
    )


@router.get("/{inventory_id}", dependencies=[Depends(get_current_user)])
def get_inventory(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    inventory_id: EntityId,
) -> Response:
    inventory = domain.get_inventory(inventory_id=inventory_id)
    return templates.TemplateResponse(
        request=request,
        name="inventories/inventory.html",
        context={"inventory": inventory},
    )


@router.post("", dependencies=[Depends(get_current_user)])
def create_inventory(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    store: Store,  # TODO: to refactor
) -> Response:
    inventory = domain.create_inventory(store=store)
    return templates.TemplateResponse(
        request=request,
        name="inventories/_inventory_row.html",
        context={"inventory": inventory},
    )


@router.get("/{inventory_id}/delete", dependencies=[Depends(get_current_user)])
def delete_inventory(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    inventory_id: EntityId,
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
    store: Store,  # TODO: to refactor
    category: Annotated[str, Body()],
) -> Response:
    domain.reset_pos_stocks(store=store, category=category)
    return RedirectResponse(
        url=request.url_for("get_inventories_view"),
        status_code=status.HTTP_302_FOUND,
    )
