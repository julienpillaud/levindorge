from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_current_user, get_domain, get_templates
from app.api.volumes.dtos import VolumeDTO
from app.domain.domain import Domain
from app.domain.entities import EntityId
from app.domain.volumes.entities import VolumeCreate

router = APIRouter(prefix="/volumes", tags=["Volumes"])


@router.get("", dependencies=[Depends(get_current_user)])
def get_volumes(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    result = domain.get_volumes()
    return templates.TemplateResponse(
        request=request,
        name="items/volumes.html",
        context={"result": result},
    )


@router.post("", dependencies=[Depends(get_current_user)])
def create_volume(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    volume_request: VolumeDTO,
) -> Response:
    volume_create = VolumeCreate(**volume_request.model_dump())
    volume = domain.create_volume(volume_create)

    response = templates.TemplateResponse(
        request=request,
        name="items/_volume_row.html",
        context={"item": volume},
    )
    response.headers["X-Display-Name"] = volume.display_name
    return response


@router.delete("/{volume_id}", dependencies=[Depends(get_current_user)])
def delete_volume(
    domain: Annotated[Domain, Depends(get_domain)],
    volume_id: EntityId,
) -> None:
    domain.delete_volume(volume_id=volume_id)
