import pytest
from bson import ObjectId
from cleanstack.exceptions import NotFoundError

from app.domain.context import ContextProtocol
from app.domain.exceptions import EntityInUseError
from app.domain.origins.commands import delete_origin_command
from tests.factories.articles import ArticleFactory
from tests.factories.origins import OriginFactory


def test_delete_origin(
    context: ContextProtocol,
    origin_factory: OriginFactory,
) -> None:
    origin = origin_factory.create_one()

    delete_origin_command(context, origin_id=origin.id)

    assert context.origin_repository.get_by_id(origin.id) is None


def test_delete_origin_not_found(context: ContextProtocol) -> None:
    with pytest.raises(NotFoundError):
        delete_origin_command(context, origin_id=str(ObjectId()))


def test_delete_origin_in_use(
    context: ContextProtocol,
    article_factory: ArticleFactory,
    origin_factory: OriginFactory,
) -> None:
    origin_name = "Origin 1"
    origin = origin_factory.create_one(name=origin_name)
    article_factory.create_one(origin=origin_name)

    with pytest.raises(EntityInUseError):
        delete_origin_command(context, origin_id=origin.id)
