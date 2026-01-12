import pytest
from bson import ObjectId
from cleanstack.exceptions import NotFoundError

from app.domain.context import ContextProtocol
from app.domain.distributors.commands import delete_distributor_command
from app.domain.exceptions import EntityInUseError
from tests.factories.articles import ArticleFactory
from tests.factories.distributors import DistributorFactory


def test_delete_distributor(
    context: ContextProtocol,
    distributor_factory: DistributorFactory,
) -> None:
    distributor = distributor_factory.create_one()

    delete_distributor_command(context, distributor_id=distributor.id)

    assert context.distributor_repository.get_by_id(distributor.id) is None


def test_delete_distributor_not_found(context: ContextProtocol) -> None:
    with pytest.raises(NotFoundError):
        delete_distributor_command(context, distributor_id=str(ObjectId()))


def test_delete_distributor_in_use(
    context: ContextProtocol,
    article_factory: ArticleFactory,
    distributor_factory: DistributorFactory,
) -> None:
    distributor_name = "Distributor 1"
    article_factory.create_one(distributor=distributor_name)
    distributor = distributor_factory.create_one(name=distributor_name)

    with pytest.raises(EntityInUseError):
        delete_distributor_command(context, distributor_id=distributor.id)
