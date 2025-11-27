from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.auth.dependencies import get_current_user
from app.api.dependencies import get_domain, get_templates
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
    result = domain.get_deposits()
    return templates.TemplateResponse(
        request=request,
        name="items/deposits.html",
        context={
            "current_user": current_user,
            "deposits": result.items,
        },
    )
