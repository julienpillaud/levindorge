from pydantic import BaseModel

from app.domain.producers.entities import ProducerType


class ProducerDTO(BaseModel):
    name: str
    type: ProducerType
