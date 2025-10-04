from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_domain
from app.app.auth.dependencies import get_current_user
from app.app.dependencies import get_templates
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
    form_data: Annotated[DepositCreate, Form()],
) -> Response:
    domain.create_deposit(deposit_create=form_data)
    return RedirectResponse(
        url=request.url_for("get_deposits_view"),
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/{deposit_id}/delete", dependencies=[Depends(get_current_user)])
def delete_deposit(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    deposit_id: str,
) -> Response:
    domain.delete_deposit(deposit_id=deposit_id)
    return RedirectResponse(
        url=request.url_for("get_deposits_view"),
        status_code=status.HTTP_302_FOUND,
    )
