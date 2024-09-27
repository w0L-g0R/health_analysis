from abc import ABC, abstractmethod


class TaskDelete(ABC):
    @abstractmethod
    async def delete(self, incoming_event_data: bytes):
        pass
