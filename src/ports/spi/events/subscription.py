from abc import ABC, abstractmethod


class EventSubscription(ABC):
    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass
