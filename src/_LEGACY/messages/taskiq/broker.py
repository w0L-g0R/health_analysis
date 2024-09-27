import logging
from typing import Callable, Dict

from taskiq_aio_pika import AioPikaBroker

from src.config.config import setup_logging
from src.config.field_validator import FieldValidator
from src._LEGACY.messages.broker import MessageBroker

setup_logging()
logger = logging.getLogger(__name__)


class TaskiqBroker(
    FieldValidator,
    AioPikaBroker,
    MessageBroker,
):
    url: str
    name: str
    exchange_name: str
    queue_name: str
    tasks: Dict[str, Callable]

    def __init__(self, **data):
        print(data)
        pass
        # super().__init__(
        #     **data,
        #     declare_exchange=True,
        #     declare_queues=True,
        # )

    def register_tasks(self):
        for name, func in self.tasks.items():
            self.register_task(
                name=name,
                func=func,
            )

    async def startup(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    def __repr__(self):
        return f"""Broker:
         type: {self.type}, 
         id: {id(self)}, 
         exchange_name: {self._exchange_name}, 
         queue_name: {self._queue_name}, 
         tasks: {list(self.tasks.keys())})"
        """
