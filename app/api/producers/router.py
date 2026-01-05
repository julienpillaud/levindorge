from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_current_user, get_domain, get_templates
from app.api.producers.dtos import ProducerDTO
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
    result = domain.get_producers(producer_type=producer_type)
    return templates.TemplateResponse(
        request=request,
        name="items/producers.html",
        context={
            "result": result,
            "producer_type": producer_type,
            "title": TITLE_MAPPING[producer_type],
        },
    )


@router.post("", dependencies=[Depends(get_current_user)])
def create_producer(
    request: Request,
    domain: Annotated[Domain, Depends(get_domain)],
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    producer_create: ProducerDTO,
) -> Response:
    producer = domain.create_producer(
        name=producer_create.name,
        producer_type=producer_create.type,
    )

    response = templates.TemplateResponse(
        request=request,
        name="items/_producer_row.html",
        context={"item": producer},
    )
    response.headers["X-Display-Name"] = producer.display_name
    return response


@router.delete("/{producer_id}", dependencies=[Depends(get_current_user)])
def delete_producer(
    domain: Annotated[Domain, Depends(get_domain)],
    producer_id: str,
) -> None:
    domain.delete_producer(producer_id=producer_id)
