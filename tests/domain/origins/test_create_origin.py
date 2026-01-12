import pytest

from app.domain.context import ContextProtocol
from app.domain.exceptions import AlreadyExistsError
from app.domain.origins.commands import create_origin_command
from app.domain.origins.entities import OriginCreate
from tests.factories.origins import OriginFactory


def test_create_origin(
    context: ContextProtocol,
    origin_factory: OriginFactory,
) -> None:
    origin_data = origin_factory.build()
    origin_create = OriginCreate(
        name=origin_data.name,
        code=origin_data.code,
        type=origin_data.type,
    )
    origin = create_origin_command(context, origin_create=origin_create)

    assert origin.name == origin_create.name
    assert origin.code == origin_create.code
    assert origin.type == origin_create.type


def test_create_origin_already_exists(
    context: ContextProtocol,
    origin_factory: OriginFactory,
) -> None:
    origin = origin_factory.create_one()
    with pytest.raises(AlreadyExistsError):
        create_origin_command(
            context,
            origin_create=OriginCreate(
                name=origin.name,
                code=origin.code,
                type=origin.type,
            ),
        )
