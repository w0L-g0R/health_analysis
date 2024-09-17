import abc
import enum

from taskiq_aio_pika import AioPikaBroker


class EventHandler(abc.ABC):
    async def handle(self, event):
        pass
