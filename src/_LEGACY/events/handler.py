from abc import ABC, abstractmethod

from src._LEGACY.events.subscription import EventSubscription


class EventsHandler(ABC):
    @abstractmethod
    async def handle(self, subscription: EventSubscription):
        pass
