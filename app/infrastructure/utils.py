from collections.abc import Iterator
from typing import Any


def iter_dicts(value: dict[Any, Any]) -> Iterator[dict[Any, Any]]:
    stack: list[Any] = [value]

    while stack:
        node = stack.pop()

        if isinstance(node, dict):
            yield node
            stack.extend(node.values())

        elif isinstance(node, list):
            stack.extend(node)
