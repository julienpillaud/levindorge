from app.domain.context import ContextProtocol
from app.domain.producers.commands import get_producers_command
from app.domain.producers.entities import ProducerType
from tests.factories.producers import ProducerFactory


def test_get_producers(
    context: ContextProtocol,
    producer_factory: ProducerFactory,
) -> None:
    producers_count = 3
    producer_factory.create_many(producers_count)

    result = get_producers_command(context)

    assert result.total == producers_count
    producers = result.items
    assert len(producers) == producers_count


def test_get_producers_by_type(
    context: ContextProtocol,
    producer_factory: ProducerFactory,
) -> None:
    producers_count = 3
    producer_factory.create_many(producers_count, type=ProducerType.DISTILLERY)
    producer_factory.create_one(type=ProducerType.BREWERY)

    result = get_producers_command(context, producer_type=ProducerType.BREWERY)

    assert result.total == 1
    producers = result.items
    assert len(producers) == 1
