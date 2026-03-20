from enum import StrEnum

from cleanstack.entities import DomainEntity


class ProducerType(StrEnum):
    BREWERY = "brewery"
    DISTILLERY = "distillery"


class Producer(DomainEntity):
    name: str
    type: ProducerType | None
