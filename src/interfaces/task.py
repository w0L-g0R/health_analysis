from abc import ABC, abstractmethod


class Task(ABC):

    @abstractmethod
    async def execute(self, **kwargs):
        raise NotImplementedError("Method not implemented")
