from abc import ABC, abstractmethod


class Task(ABC):

    @abstractmethod
    def set_task(self, func):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def execute(self, **kwargs):
        raise NotImplementedError("Method not implemented")
