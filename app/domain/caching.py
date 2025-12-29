import hashlib
import json
import logging
from collections.abc import Callable
from functools import wraps

from pydantic import BaseModel

from app.domain.context import ContextProtocol
from app.domain.types import Command

logger = logging.getLogger(__name__)


def cached_command[**P, R: BaseModel](
    response_model: type[R],
    ttl: int = 3600,
    tag: str | None = None,
) -> Callable[[Command[P, R]], Command[P, R]]:
    def decorator(func: Command[P, R]) -> Command[P, R]:
        @wraps(func)
        def wrapper(
            context: ContextProtocol,
            /,
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> R:
            key = build_cache_key(func, *args, **kwargs)
            cached = context.cache_manager.get(key=key)
            if cached:
                logger.debug(f"Cache hit for key: {key}")
                return response_model.model_validate_json(cached)

            result = func(context, *args, **kwargs)
            context.cache_manager.set(
                key=key,
                value=result.model_dump_json(),
                ttl=ttl,
                tag=tag,
            )
            return result

        return wrapper

    return decorator


def build_cache_key[**P, R: BaseModel](
    func: Command[P, R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> str:
    payload = json.dumps(
        {
            "args": args,
            "kwargs": dict(sorted(kwargs.items())),
        },
        default=str,
        separators=(",", ":"),
    )

    digest = hashlib.sha256(payload.encode()).hexdigest()[:16]
    return f"{func.__name__}:{digest}"
