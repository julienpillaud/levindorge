import pytest
from bson import ObjectId
from cleanstack.exceptions import NotFoundError

from app.domain.context import ContextProtocol
from app.domain.exceptions import EntityInUseError
from app.domain.producers.commands import delete_producer_command
from tests.factories.articles import ArticleFactory
from tests.factories.producers import ProducerFactory


def test_delete_producer(
    context: ContextProtocol,
    producer_factory: ProducerFactory,
) -> None:
    producer = producer_factory.create_one()

    delete_producer_command(context, producer_id=producer.id)

    assert context.producer_repository.get_by_id(producer.id) is None


def test_delete_producer_not_found(
    context: ContextProtocol, producer_factory: ProducerFactory
) -> None:
    with pytest.raises(NotFoundError):
        delete_producer_command(context, producer_id=str(ObjectId()))


def test_delete_producer_in_use(
    context: ContextProtocol,
    article_factory: ArticleFactory,
    producer_factory: ProducerFactory,
) -> None:
    producer = producer_factory.create_one()
    article_factory.create_one(producer=producer.name)

    with pytest.raises(EntityInUseError):
        delete_producer_command(context, producer_id=producer.id)
