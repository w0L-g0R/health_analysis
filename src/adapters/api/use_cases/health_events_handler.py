# import logging
#
# from dependency_injector.wiring import Closing, Provide, inject
#
# from src._LEGACY.events.handler import EventsHandler
# from src.config.config import setup_logging
# from src.config.field_validator import FieldValidator
#
# setup_logging()
# logger = logging.getLogger(__name__)
#
#
# class HealthEventsHandler(FieldValidator):
#
#     @handle_exceptions
#     @inject
#     async def handle(
#         self, subscription: EventSubscription = Closing[Provide["event_subscription"]]
#     ):
#         return NotImplemented
