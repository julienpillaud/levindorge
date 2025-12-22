from app.domain.context import ContextProtocol
from app.domain.distributors.commands import get_distributors_command
from tests.factories.distributors import DistributorFactory


def test_get_distributors(
    context: ContextProtocol,
    distributor_factory: DistributorFactory,
) -> None:
    distributors_count = 3
    distributor_factory.create_many(distributors_count)

    result = get_distributors_command(context)

    assert result.total == distributors_count
    distributors = result.items
    assert len(distributors) == distributors_count
