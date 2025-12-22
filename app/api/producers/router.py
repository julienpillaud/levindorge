from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_current_user, get_domain, get_templates
from app.domain.domain import Domain
from app.domain.producers.entities import ProducerType

TITLE_MAPPING = {
    ProducerType.BREWERY: "Brasseries",
    ProducerType.DISTILLERY: "Distilleries",
}

router = APIRouter(prefix="/producers", tags=["Producers"])


@router.get("/{producer_type}", dependencies=[Depends(get_current_user)])
def get_producers(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    producer_type: ProducerType,
) -> Response:
    producers = domain.get_producers(producer_type=producer_type)
    return templates.TemplateResponse(
        request=request,
        name="items/items.html",
        context={
            "items": producers.items,
            "title": TITLE_MAPPING[producer_type],
        },
    )
