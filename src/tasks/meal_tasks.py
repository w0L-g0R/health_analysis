# import asyncio
from enum import Enum
from pathlib import Path
from typing import Annotated

from src.config.config import BASE_DIR_PATH, get_module_path

from taskiq import Context, TaskiqDepends

from src.dependencies.meals.factories import MealQueryFactory
from src.domains.meals.events import InsertMealEvent, MealEvents


class MealsTasks:
    @staticmethod
    async def insert_meal(
        event: str,
        context: Annotated[Context, TaskiqDepends()],
    ):
        try:
            print("event", event)
            # print("state", context.state)
        except Exception as e:
            print(e)
        # event_type = context.state.events().get(MealEvents.INSERT)
        # database = context.state.database
        # query_factory = context.state.query_factories().get(MealQueryFactory.INSERT)
        # validated_event = event_type.model_validate(event)
        # query = query_factory.create(from_event=validated_event)

        # await database.execute(query.statement, query.args)


class MealTaskPath(Enum):
    INSERT = f"{get_module_path(__file__)}:{MealsTasks.insert_meal.__name__}"
