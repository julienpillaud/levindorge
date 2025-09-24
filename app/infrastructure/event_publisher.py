import asyncio

from faststream.redis import RedisBroker

from app.domain.protocols.event_publisher import EventPublisherProtocol


class FastStreamEventPublisher(EventPublisherProtocol):
    def __init__(self, broker: RedisBroker):
        self.broker = broker

    async def _publish(self, channel: str, message: str) -> None:
        async with self.broker as broker:
            await broker.publish(channel=channel, message=message)

    def publish(self, channel: str, message: str) -> None:
        asyncio.run(self._publish(channel=channel, message=message))
