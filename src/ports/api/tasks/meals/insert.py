from abc import ABC, abstractmethod

from src.config.validation import FieldValidator


class TaskInsert(ABC, FieldValidator):
    @abstractmethod
    async def insert(self, incoming_event_data: bytes):
        pass
