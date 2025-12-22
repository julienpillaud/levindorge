from app.domain.context import ContextProtocol
from app.domain.origins.commands import get_origins_command
from tests.factories.origins import OriginFactory


def test_get_origins(context: ContextProtocol, origin_factory: OriginFactory) -> None:
    origins_count = 3
    origin_factory.create_many(origins_count)

    result = get_origins_command(context)

    assert result.total == origins_count
    origins = result.items
    assert len(origins) == origins_count
