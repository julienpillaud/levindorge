from app.domain._shared.entities import ProducerType
from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse
from app.domain.producers.entities import Producer


def get_producers_command(
    context: ContextProtocol,
    producer_type: ProducerType,
) -> PaginatedResponse[Producer]:
    return context.producer_repository.get_all(
        filters={"type": producer_type},
        sort={"name": 1},
        limit=300,
    )
