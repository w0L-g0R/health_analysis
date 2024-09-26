from abc import ABC, abstractmethod


class EventClient(ABC):

    @property
    @abstractmethod
    def subscription(self) -> None:
        pass
