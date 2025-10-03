from cleanstack.exceptions import ForbiddenError

from app.domain.items.entities import ItemType


class UserUnauthorizedError(ForbiddenError):
    pass


class POSManagerError(Exception):
    pass


# special case to put an error message in the session
class CannotDeleteError(Exception):
    def __init__(self, item_name: str, item_type: ItemType | None = None):
        self.item_name = item_name
        self.item_type = item_type


class ItemInUseError(CannotDeleteError):
    def __init__(self, item_name: str, item_type: ItemType | None):
        super().__init__(item_name=item_name, item_type=item_type)


class VolumeInUseError(CannotDeleteError):
    def __init__(self, item_name: str):
        super().__init__(item_name=item_name)


class DepositInUseError(CannotDeleteError):
    def __init__(self, item_name: str):
        super().__init__(item_name=item_name)
