from abc import ABC, abstractmethod

from pydantic import BaseModel


class TaskInsert(ABC, BaseModel):
    @abstractmethod
    async def insert(self, incoming_event_data: bytes):
        pass
