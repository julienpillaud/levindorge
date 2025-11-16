from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.auth.dependencies import get_current_user
from app.api.dependencies import get_domain, get_templates
from app.domain.domain import Domain
from app.domain.users.entities import User
from app.domain.volumes.entities import VolumeCreate

router = APIRouter(prefix="/volumes")


@router.get("")
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


@router.post("", dependencies=[Depends(get_current_user)])
def create_volume(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    form_data: Annotated[VolumeCreate, Form()],
) -> Response:
    item = domain.create_volume(volume_create=form_data)
    return templates.TemplateResponse(
        request=request,
        name="items/_volume_row.html",
        context={"volume": item},
    )


@router.delete("/{volume_id}", dependencies=[Depends(get_current_user)])
def delete_volume(
    domain: Annotated[Domain, Depends(get_domain)],
    volume_id: str,
) -> Response:
    domain.delete_volume(volume_id=volume_id)
    return Response(status_code=status.HTTP_200_OK)
