from cleanstack.exceptions import ForbiddenError


class UserUnauthorizedError(ForbiddenError):
    pass


class POSManagerError(Exception):
    pass


# special case to put an error message in the session
class CannotDeleteError(Exception):
    def __init__(self, item_name: str):
        self.item_name = item_name


class VolumeInUseError(CannotDeleteError):
    def __init__(self, item_name: str):
        super().__init__(item_name=item_name)


class DepositInUseError(CannotDeleteError):
    def __init__(self, item_name: str):
        super().__init__(item_name=item_name)
