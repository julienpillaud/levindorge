from typing import Any, Protocol


class EventPublisherProtocol(Protocol):
    def publish(self, channel: str, message: Any) -> None: ...
