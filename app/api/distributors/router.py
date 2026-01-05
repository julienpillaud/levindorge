from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_current_user, get_domain, get_templates
from app.api.distributors.dtos import DistributorDTO
from app.domain.domain import Domain

router = APIRouter(prefix="/distributors", tags=["Distributors"])


@router.get("", dependencies=[Depends(get_current_user)])
def get_distributors(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    result = domain.get_distributors()
    return templates.TemplateResponse(
        request=request,
        name="items/distributors.html",
        context={"result": result},
    )


@router.post("", dependencies=[Depends(get_current_user)])
def create_distributor(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    distributor_create: DistributorDTO,
) -> Response:
    distributor = domain.create_distributor(name=distributor_create.name)

    response = templates.TemplateResponse(
        request=request,
        name="items/_distributor_row.html",
        context={"item": distributor},
    )
    response.headers["X-Display-Name"] = distributor.display_name
    return response


@router.delete("/{distributor_id}", dependencies=[Depends(get_current_user)])
def delete_distributor(
    domain: Annotated[Domain, Depends(get_domain)],
    distributor_id: str,
) -> None:
    domain.delete_distributor(distributor_id=distributor_id)
