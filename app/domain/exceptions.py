from cleanstack.exceptions import ConflictError, ForbiddenError


class UserUnauthorizedError(ForbiddenError):
    pass


class POSManagerError(Exception):
    pass


class AlreadyExistsError(ConflictError):
    def __init__(self, message: str, display_name: str):
        self.display_name = display_name
        super().__init__(message)


class EntityInUseError(ConflictError):
    def __init__(self, message: str, display_name: str):
        self.display_name = display_name
        super().__init__(message)
