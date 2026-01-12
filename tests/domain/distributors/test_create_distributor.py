import pytest

from app.domain.context import ContextProtocol
from app.domain.distributors.commands import create_distributor_command
from app.domain.exceptions import AlreadyExistsError
from tests.factories.distributors import DistributorFactory


def test_create_distributor(
    context: ContextProtocol,
    distributor_factory: DistributorFactory,
) -> None:
    distributor = create_distributor_command(context, name="New Distributor")

    assert distributor.name == "New Distributor"


def test_create_distributor_already_exists(
    context: ContextProtocol,
    distributor_factory: DistributorFactory,
) -> None:
    distributor = distributor_factory.create_one()
    with pytest.raises(AlreadyExistsError):
        create_distributor_command(context, name=distributor.name)
