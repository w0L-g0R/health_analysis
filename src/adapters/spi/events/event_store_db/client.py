import logging
from typing import Optional

from dependency_injector.resources import Resource, T
from esdbclient import EventStoreDBClient
from pydantic import Field, PrivateAttr

from src.config.config import setup_logging
from src.config.field_validator import FieldValidator

setup_logging()
logger = logging.getLogger(__name__)


class EventStoreDbClient(EventStoreDBClient):

    # _stream_name: str = PrivateAttr()
    # _subscribe_from_end: bool = PrivateAttr()
    # _is_closed: bool = PrivateAttr(default=False)

    def __init__(self, uri: str, stream_name: str, subscribe_from_end: bool):
        # super().__init__()
        super().__init__(
            uri=uri,
        )
        # self._stream_name = stream_name
        # self._subscribe_from_end = subscribe_from_end

    # @property
    # def subscription(self) -> Optional[AbstractCatchupSubscription]:
    #     try:
    #         return self.subscribe_to_stream(
    #             stream_name=self._stream_name,
    #             from_end=self._subscribe_from_end,
    #         )
    #     except Exception as e:
    #         print(e)

    # def shutdown(self, **kwargs) -> None:
    #     self.close()
    #     self._is_closed = True
    #     print("EventStoreDbClient is_closed: ", self._is_closed)
    #     logger.info(f"Closed event bus client {id(self)}: {self._is_closed}")
