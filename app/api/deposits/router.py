from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.auth.dependencies import get_current_user
from app.api.dependencies import get_domain, get_templates
from app.domain.deposits.entities import DepositCreate
from app.domain.domain import Domain
from app.domain.users.entities import User

router = APIRouter(prefix="/deposits")


@router.get("")
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


@router.post("", dependencies=[Depends(get_current_user)])
def create_deposit(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    form_data: Annotated[DepositCreate, Form()],
) -> Response:
    item = domain.create_deposit(deposit_create=form_data)
    return templates.TemplateResponse(
        request=request,
        name="items/_deposit_row.html",
        context={"deposit": item},
    )


@router.delete("/{deposit_id}", dependencies=[Depends(get_current_user)])
def delete_deposit(
    domain: Annotated[Domain, Depends(get_domain)],
    deposit_id: str,
) -> Response:
    domain.delete_deposit(deposit_id=deposit_id)
    return Response(status_code=status.HTTP_200_OK)
