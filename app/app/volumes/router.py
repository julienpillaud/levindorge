from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_domain
from app.app.auth.dependencies import get_current_user
from app.app.dependencies import get_templates
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
    form_data: Annotated[VolumeCreate, Form()],
) -> Response:
    domain.create_volume(volume_create=form_data)
    return RedirectResponse(
        url=request.url_for("get_volumes_view"),
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/{volume_id}/delete", dependencies=[Depends(get_current_user)])
def delete_volume(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    volume_id: str,
) -> Response:
    domain.delete_volume(volume_id=volume_id)
    return RedirectResponse(
        url=request.url_for("get_volumes_view"),
        status_code=status.HTTP_302_FOUND,
    )
