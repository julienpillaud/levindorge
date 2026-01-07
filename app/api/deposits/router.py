from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_current_user, get_domain, get_templates
from app.api.deposits.dtos import DepositDTO
from app.domain.deposits.entities import DepositCreate
from app.domain.domain import Domain
from app.domain.entities import EntityId

router = APIRouter(prefix="/deposits", tags=["Deposits"])


@router.get("", dependencies=[Depends(get_current_user)])
def get_deposits(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
) -> Response:
    result = domain.get_deposits()
    return templates.TemplateResponse(
        request=request,
        name="items/deposits.html",
        context={"result": result},
    )


@router.post("", dependencies=[Depends(get_current_user)])
def create_deposit(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    deposit_request: DepositDTO,
) -> Response:
    deposit_create = DepositCreate(**deposit_request.model_dump())
    deposit = domain.create_deposit(deposit_create)

    response = templates.TemplateResponse(
        request=request,
        name="items/_deposit_row.html",
        context={"item": deposit},
    )
    response.headers["X-Display-Name"] = deposit.display_name
    return response


@router.delete("/{deposit_id}", dependencies=[Depends(get_current_user)])
def delete_deposit(
    domain: Annotated[Domain, Depends(get_domain)],
    deposit_id: EntityId,
) -> None:
    domain.delete_deposit(deposit_id=deposit_id)
