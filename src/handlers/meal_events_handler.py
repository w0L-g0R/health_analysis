import logging

from esdbclient.common import AbstractCatchupSubscription

from src.events.meals.add_meal_event import AddMealEvent
from src.config.config import setup_logging
from src.config.field_validator import FieldValidator

setup_logging()
logger = logging.getLogger(__name__)

import functools
import logging

from src.config.config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def handle_exceptions(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except KeyboardInterrupt as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise e

    return wrapper


class MealsEventsHandler(FieldValidator):
    subscription: AbstractCatchupSubscription
    add_meal_event: str

    @handle_exceptions
    async def handle_events(self, tasks: dict):
        while True:
            for event in self.subscription:
                print("Event", event)
                # data = json.loads(event.data.decode("utf-8"))

                match event.type:
                    case self.add_meal_event:
                        task = tasks.get(AddMealEvent.__name__)
                        print("Task", task)
                        await task.execute(data=event.data)

                    # case self.remove_meal_event_type:
                    #     await self.remove_meal_use_case.remove_meal(dto)

                    case _:
                        pass
