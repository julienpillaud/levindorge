from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_current_user, get_domain, get_templates
from app.api.origins.dtos import OriginDTO
from app.domain.domain import Domain
from app.domain.entities import EntityId
from app.domain.origins.entities import OriginCreate

router = APIRouter(prefix="/origins", tags=["Origins"])


@router.get("", dependencies=[Depends(get_current_user)])
def get_origins(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    result = domain.get_origins()
    return templates.TemplateResponse(
        request=request,
        name="items/origins.html",
        context={"result": result},
    )


@router.post("", dependencies=[Depends(get_current_user)])
def create_origin(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    origin_request: OriginDTO,
) -> Response:
    origin_create = OriginCreate(**origin_request.model_dump())
    origin = domain.create_origin(origin_create)

    response = templates.TemplateResponse(
        request=request,
        name="items/_origin_row.html",
        context={"item": origin},
    )
    response.headers["X-Display-Name"] = origin.display_name
    return response


@router.delete("/{origin_id}", dependencies=[Depends(get_current_user)])
def delete_origin(
    domain: Annotated[Domain, Depends(get_domain)],
    origin_id: EntityId,
) -> None:
    domain.delete_origin(origin_id=origin_id)
