from abc import ABC, abstractmethod

from src.ports.spi.events.subscription import EventSubscription


class EventsHandler(ABC):
    @abstractmethod
    async def handle(self, subscription: EventSubscription):
        pass
