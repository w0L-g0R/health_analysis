from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID


class Repository(ABC):
    @abstractmethod
    async def __ainit__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def insert(self, *args) -> None:
        pass

    @abstractmethod
    async def delete(self, *kwargs) -> None:
        pass

    @abstractmethod
    async def update(self, *args) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass
