import asyncio
from typing import Any

from faststream.redis import RedisBroker

from app.domain._shared.protocols.event_publisher import EventPublisherProtocol


class FastStreamEventPublisher(EventPublisherProtocol):
    def __init__(self, broker: RedisBroker):
        self.broker = broker

    async def _publish(self, channel: str, message: Any) -> None:
        async with self.broker as broker:
            await broker.publish(channel=channel, message=message)

    def publish(self, channel: str, message: Any) -> None:
        asyncio.run(self._publish(channel=channel, message=message))
