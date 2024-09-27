import json
import logging

from esdbclient.common import AbstractCatchupSubscription

from src.adapters.api.tasks.taskiq.meal_tasks import MealTasks
from src.adapters.api.use_cases.exceptions import handle_exceptions
from src.adapters.spi.events.meal_events import MealEvents
from src.config.config import setup_logging
from src.config.field_validator import FieldValidator

setup_logging()
logger = logging.getLogger(__name__)


class MealsEventsHandler(FieldValidator):
    subscription: AbstractCatchupSubscription

    @handle_exceptions
    async def handle_events(self, tasks: MealTasks, events: MealEvents):
        while True:
            print("Handling events")
            for event in self.subscription:
                print("Event", event)
                data = json.loads(event.data.decode("utf-8"))

                match event.type:
                    case events.add_meal:
                        print("Event Type", events.add_meal)
                        await tasks.add_meal.execute(data=data)

                    # case self.remove_meal_event_type:
                    #     await self.remove_meal_use_case.remove_meal(dto)

                    case _:
                        pass
