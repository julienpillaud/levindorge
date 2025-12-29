from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_current_user, get_domain, get_templates
from app.domain.domain import Domain

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
