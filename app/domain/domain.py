import logging
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import wraps
from typing import Concatenate, ParamSpec, Protocol, TypeVar

from app.domain.articles.commands import (
    create_article_command,
    delete_article_command,
    get_article_command,
    get_articles_command,
    update_article_command,
)
from app.domain.commons.commands import (
    get_template_context_command,
    get_type_infos_command,
)
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
            start_time = time.perf_counter()
            with self.context.transaction():
                try:
                    result = func(self.context, *args, **kwargs)
                except DomainError as error:
                    self.context.rollback()
                    logger.debug(
                        f"Command '{func.__name__}' failed with "
                        f"{error.__class__.__name__}: {error}"
                    )
                    raise error

                self.context.commit()
                duration = time.perf_counter() - start_time
                logger.debug(
                    f"Command '{func.__name__}' succeeded in {duration * 1000:.1f} ms",
                )
                return result

        return wrapper

    def __init__(self, context: TransactionalContextProtocol):
        self.context = context

        self.get_user_by_email = self.command_handler(get_user_by_email_command)
        self.get_articles = self.command_handler(get_articles_command)
        self.get_article = self.command_handler(get_article_command)
        self.create_article = self.command_handler(create_article_command)
        self.update_article = self.command_handler(update_article_command)
        self.delete_article = self.command_handler(delete_article_command)

        self.get_type_infos = self.command_handler(get_type_infos_command)
        self.get_template_context = self.command_handler(get_template_context_command)
