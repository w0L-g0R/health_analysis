import logging
from typing import Callable, Dict

from pydantic import BaseModel
from taskiq_aio_pika import AioPikaBroker

from src.config.config import setup_logging
from src.ports.spi.messages.broker import MessageBroker

setup_logging()
logger = logging.getLogger(__name__)


class TaskiqBroker(AioPikaBroker, MessageBroker):
    url: str
    name: str
    tasks: Dict[str, Callable]
    exchange_name: str
    queue_name: str

    def connect(self):
        super().__init__(
            url=self.url,
            exchange_name=self.exchange_name,
            queue_name=self.queue_name,
            declare_exchange=True,
            declare_queues=True,
        )

        return self

    def register_tasks(self, tasks: Dict[str, Callable]):
        for name, func in self.tasks.items():
            self.register_task(
                name=name,
                func=func,
            )

    def __repr__(self):
        return f"""Broker:
         type: {self.type}, 
         id: {id(self)}, 
         exchange_name: {self._exchange_name}, 
         queue_name: {self._queue_name}, 
         tasks: {list(self.tasks.keys())})"
        """
