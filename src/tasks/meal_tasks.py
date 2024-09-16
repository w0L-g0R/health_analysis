# import asyncio
from enum import Enum
from pathlib import Path
from typing import Annotated

from src.config import BASE_DIR_PATH, get_module_path

from taskiq import Context, TaskiqDepends

from src.dependencies.meals.factories import MealQueryFactory
from src.domains.meals.events import InsertMealEvent, MealEvents


async def insert_meal(
    event: InsertMealEvent,
    context: Annotated[Context, TaskiqDepends()],
):
    event_type = context.state.events().get(MealEvents.INSERT)
    database = context.state.database
    query_factory = context.state.query_factories().get(MealQueryFactory.INSERT)
    validated_event = event_type.model_validate(event)
    query = query_factory.create(from_event=validated_event)

    await database.execute(query.statement, query.args)


class MealTasks(Enum):
    INSERT = f"{get_module_path(__file__)}:{insert_meal.__name__}"
