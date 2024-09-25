from abc import ABC, abstractmethod
from typing import Callable, Dict

from pydantic import BaseModel


class MessageBroker(ABC, BaseModel):
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def register_tasks(self, tasks: Dict[str, Callable]) -> None:
        pass

    @abstractmethod
    async def startup(self) -> None:
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass
