import logging

from dependency_injector.wiring import Closing, Provide, inject

from src.config.config import setup_logging
from src.config.validation import FieldValidator
from src.handler.exceptions import handle_exceptions
from src.ports.api.tasks.meals.delete import TaskDelete
from src.ports.api.tasks.meals.insert import TaskInsert
from src.ports.spi.events.handler import EventsHandler
from src.ports.spi.events.subscription import EventSubscription

setup_logging()
logger = logging.getLogger(__name__)


class MealsEventsHandler(EventsHandler, FieldValidator):
    meal_insert_task: TaskInsert
    meal_delete_task: TaskDelete
    meal_insert_event_type_name: str
    meal_delete_event_type_name: str

    @handle_exceptions
    @inject
    async def handle(
        self, subscription: EventSubscription = Closing[Provide["event_subscription"]]
    ):
        while True:
            for event in subscription:

                match event.type:
                    case self.meal_insert_event_type_name:
                        await self.meal_insert_task.insert(event.data)

                    case self.meal_delete_event_type_name:
                        await self.meal_delete_task.delete(event.data)

                    case _:
                        pass
