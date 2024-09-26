import logging
from typing import Optional

from esdbclient import EventStoreDBClient
from esdbclient.common import AbstractCatchupSubscription

from src.config.config import setup_logging
from src.config.validation import FieldValidator
from src.ports.spi.events.client import EventClient

setup_logging()
logger = logging.getLogger(__name__)


class EventStoreDbClient(EventStoreDBClient, EventClient, FieldValidator):
    uri: str
    stream_name: str
    subscribe_from_end: bool

    def __init__(
        self,
    ):
        logger.info(f"Connecting to EventStoreDbClient: {self.uri}")
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
