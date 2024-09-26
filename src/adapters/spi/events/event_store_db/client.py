import logging
from typing import Optional
from esdbclient import CatchupSubscription, EventStoreDBClient
from esdbclient.common import AbstractCatchupSubscription
from pydantic import BaseModel

from src.config.config import setup_logging
from src.ports.spi.events.client import EventClient

setup_logging()
logger = logging.getLogger(__name__)


class EventStoreDbClient(EventStoreDBClient, EventClient, BaseModel):
    uri: str
    stream_name: str
    subscribe_from_end: bool

    def __init__(
        self,
    ):
        super().__init__(str(self.uri))

    @property
    def subscription(self) -> Optional[AbstractCatchupSubscription]:
        try:
            return self.subscribe_to_stream(
                stream_name=self.stream_name,
                from_end=self.subscribe_from_end,
            )
        except Exception as e:
            print(e)
