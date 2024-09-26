from esdbclient import CatchupSubscription
from esdbclient.common import AbstractCatchupSubscription

from src.ports.spi.events.subscription import EventSubscription


class EventStoreDbSubscription(
    EventSubscription, AbstractCatchupSubscription, CatchupSubscription
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def subscription_id(self) -> str:
        return self.subscription_id

    def shutdown(self):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self)
