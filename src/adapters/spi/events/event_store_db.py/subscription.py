from dataclasses import dataclass
from esdbclient import CatchupSubscription
from esdbclient.common import AbstractCatchupSubscription

from src.ports.spi.events.subscription import EventSubscription


class EventStoreDbSubscription(
    AbstractCatchupSubscription, CatchupSubscription, EventSubscription
):

    @property
    def subscription_id(self) -> str:
        return self.subscription_id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def shutdown(self):
        self.close()
