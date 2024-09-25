import logging

from dependency_injector.wiring import Closing, inject, Provide
from pydantic import BaseModel

from src.config.config import setup_logging
from src.handler.exceptions import handle_exceptions
from src.ports.spi.events.handler import EventsHandler
from src.ports.spi.events.subscription import EventSubscription

setup_logging()
logger = logging.getLogger(__name__)


class HealthEventsHandler(BaseModel, EventsHandler):

    @handle_exceptions
    @inject
    async def handle_events(
        self, subscription: EventSubscription = Closing[Provide["event_subscription"]]
    ):
        return NotImplemented
