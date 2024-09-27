import logging

from dependency_injector.wiring import Closing, Provide, inject
from src.config.config import setup_logging
from src.config.field_validator import FieldValidator
from src.handler.exceptions import handle_exceptions
from src.ports.spi.events.handler import EventsHandler
from src.ports.spi.events.subscription import EventSubscription

setup_logging()
logger = logging.getLogger(__name__)


class HealthEventsHandler(EventsHandler, FieldValidator):

    @handle_exceptions
    @inject
    async def handle(
        self, subscription: EventSubscription = Closing[Provide["event_subscription"]]
    ):
        return NotImplemented
