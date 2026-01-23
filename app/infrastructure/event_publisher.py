import asyncio

from faststream.rabbit import RabbitBroker

from app.domain.protocols.event_publisher import Event, EventPublisherProtocol


class FastStreamEventPublisher(EventPublisherProtocol):
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def _publish(self, events: list[Event]) -> None:
        async with self.broker as broker:
            tasks = [
                broker.publish(message=event.message, queue=event.queue)
                for event in events
            ]
            await asyncio.gather(*tasks)

    def publish(self, events: list[Event]) -> None:
        asyncio.run(self._publish(events=events))
