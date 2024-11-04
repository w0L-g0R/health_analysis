import json
import logging

from esdbclient.common import AbstractCatchupSubscription

from src.adapters.api.tasks.taskiq.meal_tasks import MealTasks

# from src.adapters.api.tasks.taskiq.meal_tasks import MealTasks
from src.adapters.api.use_cases.exceptions import handle_exceptions
from src.adapters.spi.events.meal_events import MealEvents
from src.config.config import setup_logging
from src.config.field_validator import FieldValidator

setup_logging()
logger = logging.getLogger(__name__)


class MealsEventsHandler(FieldValidator):
    subscription: AbstractCatchupSubscription
    events: MealEvents

    @handle_exceptions
    async def handle_events(self, tasks: dict):
        print("Handling events and tasks", tasks)
        while True:
            for event in self.subscription:
                print("Event", event)
                data = json.loads(event.data.decode("utf-8"))

                match event.type:
                    case self.events.add_meal:
                        print("Event Type", self.events.add_meal)
                        task = tasks.get(str(MealTasks.ADD_MEAL))
                        print("Task", task)
                        # await task.execute(data=data)
                        t, r = await task.execute(data=data)
                        print(t)
                        print(r)

                    # case self.remove_meal_event_type:
                    #     await self.remove_meal_use_case.remove_meal(dto)

                    case _:
                        pass
