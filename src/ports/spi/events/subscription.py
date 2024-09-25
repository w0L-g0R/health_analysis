from abc import ABC, abstractmethod

from pydantic import BaseModel


class EventSubscription(ABC, BaseModel):
    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass
