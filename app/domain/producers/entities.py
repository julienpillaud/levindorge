from app.domain._shared.entities import ProducerType
from app.domain.entities import DomainEntity


class Producer(DomainEntity):
    name: str
    type: ProducerType
