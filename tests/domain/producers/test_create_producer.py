import pytest

from app.domain.context import ContextProtocol
from app.domain.exceptions import AlreadyExistsError
from app.domain.producers.commands import create_producer_command
from app.domain.producers.entities import ProducerCreate
from tests.factories.producers import ProducerFactory


def test_create_producer(
    context: ContextProtocol,
    producer_factory: ProducerFactory,
) -> None:
    producer_data = producer_factory.build()
    producer_create = ProducerCreate(**producer_data.model_dump())

    producer = create_producer_command(context, producer_create=producer_create)

    assert producer.name == producer_create.name
    assert producer.type == producer_create.type


def test_create_producer_already_exists(
    context: ContextProtocol,
    producer_factory: ProducerFactory,
) -> None:
    producer = producer_factory.create_one()

    with pytest.raises(AlreadyExistsError):
        create_producer_command(
            context,
            producer_create=ProducerCreate(
                name=producer.name,
                type=producer.type,
            ),
        )
