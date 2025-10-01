from cleanstack.exceptions import ConflictError, ForbiddenError

from app.domain.items.entities import ItemType


class UserUnauthorizedError(ForbiddenError):
    pass


class ItemInUseError(ConflictError):
    def __init__(self, item_type: ItemType, item_name: str):
        self.item_type = item_type
        self.item_name = item_name


class POSManagerError(Exception):
    pass
