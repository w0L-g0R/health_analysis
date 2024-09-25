from abc import ABC, abstractmethod

from pydantic import BaseModel


class EventClient(ABC, BaseModel):
    @abstractmethod
    def __init__(
        self,
        uri: str,
        stream_name: str,
        subscribe_from_end: bool,
    ):
        pass

    @property
    @abstractmethod
    def subscription(self) -> None:
        pass
