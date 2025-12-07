from enum import StrEnum

from app.domain.entities import DomainEntity


class ProducerType(StrEnum):
    BREWERY = "brewery"
    DISTILLERY = "distillery"


class Producer(DomainEntity):
    name: str
    type: ProducerType
