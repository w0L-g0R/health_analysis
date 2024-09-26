from abc import ABC, abstractmethod

from pydantic import BaseModel


class EventClient(ABC):

    @property
    @abstractmethod
    def subscription(self) -> None:
        pass
