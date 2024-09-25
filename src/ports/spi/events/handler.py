from abc import ABC, abstractmethod

from src.ports.spi.events.subscription import EventSubscription


class EventsHandler(ABC):
    @abstractmethod
    async def handle_events(self, subscription: EventSubscription):
        pass
