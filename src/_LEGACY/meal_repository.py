from abc import ABC, abstractmethod


class Repository(ABC):

    @abstractmethod
    async def insert(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def update(self, *args, **kwargs) -> None:
        pass
