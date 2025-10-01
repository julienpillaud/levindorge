from cleanstack.exceptions import NotFoundError

from app.domain.context import ContextProtocol
from app.domain.entities import EntityId
from app.domain.exceptions import ItemInUseError
from app.domain.items.entities import Deposit, Item, ItemType, Volume


def get_items_command(context: ContextProtocol, item_type: ItemType) -> list[Item]:
    return context.repository.get_items(item_type=item_type)


def get_volumes_command(context: ContextProtocol) -> list[Volume]:
    return context.repository.get_volumes()


def get_deposits_command(context: ContextProtocol) -> list[Deposit]:
    return context.repository.get_deposits()


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


def delete_volume_command(context: ContextProtocol, volume_id: EntityId) -> None:
    volume = context.repository.get_volume(volume_id=volume_id)
    if not volume:
        raise NotFoundError()

    if context.repository.volume_is_used(volume=volume):
        raise ItemInUseError(item_type=ItemType.VOLUMES, item_name=volume.name)

    context.repository.delete_volume(volume=volume)


def delete_deposit_command(context: ContextProtocol, deposit_id: EntityId) -> None:
    deposit = context.repository.get_deposit(deposit_id=deposit_id)
    if not deposit:
        raise NotFoundError()

    if context.repository.deposit_is_used(deposit=deposit):
        raise ItemInUseError(item_type=ItemType.DEPOSITS, item_name=deposit.name)

    context.repository.delete_deposit(deposit=deposit)
