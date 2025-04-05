import logging
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import wraps
from typing import Concatenate, ParamSpec, Protocol, TypeVar

from app.domain.context import ContextProtocol
from app.domain.exceptions import DomainError
from app.domain.users.commands import get_user_by_email_command

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


class UnitOfWorkProtocol(Protocol):
    @contextmanager
    def transaction(self) -> Iterator[None]: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


class TransactionalContextProtocol(UnitOfWorkProtocol, ContextProtocol): ...


class Domain:
    def command_handler(
        self, func: Callable[Concatenate[TransactionalContextProtocol, P], R]
    ) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with self.context.transaction():
                try:
                    result = func(self.context, *args, **kwargs)
                except DomainError as error:
                    self.context.rollback()
                    logger.info(f"Domain error: {error} - Rolling back transaction")
                    raise error

                self.context.commit()
                return result

        return wrapper

    def __init__(self, context: TransactionalContextProtocol):
        self.context = context

        self.get_user_by_email = self.command_handler(get_user_by_email_command)
