import hashlib
import json
from collections.abc import Callable
from functools import wraps
from typing import Concatenate

from pydantic import TypeAdapter

from app.domain.context import ContextProtocol
from app.domain.logger import logger

type Command[**P, R] = Callable[Concatenate[ContextProtocol, P], R]


def cached_command[**P, R](
    return_type: type[R],
    ttl: int = 3600,
    tag: str | None = None,
) -> Callable[[Command[P, R]], Command[P, R]]:
    adapter = TypeAdapter(return_type)

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
                return adapter.validate_json(cached)

            result = func(context, *args, **kwargs)
            context.cache_manager.set(
                key=key,
                value=adapter.dump_json(result).decode(),
                ttl=ttl,
                tag=tag,
            )
            return result

        return wrapper

    return decorator


def build_cache_key[**P, R](
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
