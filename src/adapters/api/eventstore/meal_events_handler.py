import logging

from esdbclient import CatchupSubscription

from src.adapters.api.eventstore.exceptions import handle_exceptions
from src.config.config import setup_logging
from src.config.field_validator import FieldValidator
from src.ports.api.use_cases.meals.add_meal.add_meal_use_case import AddMealUseCase
from src.ports.api.use_cases.meals.remove_meal.remove_meal_use_case import (
    RemoveMealUseCase,
)

setup_logging()
logger = logging.getLogger(__name__)


class MealsEventsHandler(FieldValidator):
    add_meal_use_case: AddMealUseCase
    remove_meal_use_case: RemoveMealUseCase
    add_meal_event_type: str
    remove_meal_event_type: str

    @handle_exceptions
    async def handle_events(self, subscription: CatchupSubscription):
        while True:
            for event in subscription:
                dto = event.data.decode("utf-8")
                match event.type:
                    case self.add_meal_event_type:
                        await self.add_meal_use_case.add_meal(dto)

                    case self.remove_meal_event_type:
                        await self.remove_meal_use_case.remove_meal(dto)

                    case _:
                        pass
