class DomainError(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class NotAuthorizedError(DomainError):
    pass


class EntityNotFoundError(DomainError):
    pass
