import logging

from dependency_injector.wiring import Closing, Provide, inject
from src.config.config import setup_logging
from src.config.field_validator import FieldValidator
from src.handler.exceptions import handle_exceptions
from src._LEGACY.events import EventsHandler
from src._LEGACY.events import EventSubscription

setup_logging()
logger = logging.getLogger(__name__)


class HealthEventsHandler(EventsHandler, FieldValidator):

    @handle_exceptions
    @inject
    async def handle(
        self, subscription: EventSubscription = Closing[Provide["event_subscription"]]
    ):
        return NotImplemented
