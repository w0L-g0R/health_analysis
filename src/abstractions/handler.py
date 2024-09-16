import abc
import enum

from taskiq_aio_pika import AioPikaBroker


class EventHandler(abc.ABC):
    def __init__(self, tasks: enum.Enum) -> None:
        self.tasks = tasks

    ##
    @staticmethod
    async def handle(broker: AioPikaBroker):
        pass
