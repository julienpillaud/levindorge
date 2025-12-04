from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_current_user, get_domain, get_templates
from app.domain._shared.entities import ProducerType
from app.domain.domain import Domain
from app.domain.users.entities import User

TITLE_MAPPING = {
    ProducerType.BREWERY: "Brasseries",
    ProducerType.DISTILLERY: "Distilleries",
}

router = APIRouter(prefix="/producers")


@router.get("/{producer_type}")
def get_producers(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    producer_type: ProducerType,
) -> Response:
    producers = domain.get_producers(producer_type=producer_type)
    return templates.TemplateResponse(
        request=request,
        name="items/items.html",
        context={
            "current_user": current_user,
            "items": producers.items,
            "title": TITLE_MAPPING[producer_type],
        },
    )
