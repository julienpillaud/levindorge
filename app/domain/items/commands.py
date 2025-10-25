from cleanstack.exceptions import ConflictError, NotFoundError

from app.domain.context import ContextProtocol
from app.domain.entities import EntityId
from app.domain.exceptions import ItemInUseError
from app.domain.items.entities import Item, ItemCreate, ItemType


def get_items_command(context: ContextProtocol, item_type: ItemType) -> list[Item]:
    return context.repository.get_items(item_type=item_type)


def create_item_command(
    context: ContextProtocol,
    item_type: ItemType,
    item_create: ItemCreate,
) -> Item:
    item = Item(id="", name=item_create.name, demonym=item_create.demonym)

    if context.repository.item_exists(item_type=item_type, item=item):
        raise ConflictError()

    return context.repository.create_item(item_type=item_type, item=item)


def delete_item_command(
    context: ContextProtocol,
    item_type: ItemType,
    item_id: EntityId,
) -> None:
    item = context.repository.get_item(item_type=item_type, item_id=item_id)
    if not item:
        raise NotFoundError()

    if context.repository.item_is_used(item_type=item_type, item=item):
        raise ItemInUseError(item_type=item_type, item_name=item.name)

    context.repository.delete_item(item_type=item_type, item=item)
