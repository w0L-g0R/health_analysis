from abc import ABC, abstractmethod

from pydantic import BaseModel


class TaskDelete(ABC, BaseModel):
    @abstractmethod
    async def delete(self, incoming_event_data: bytes):
        pass
