# import asyncio
import asyncio
from enum import Enum
from pathlib import Path
from typing import Annotated

from config.config import BASE_DIR_PATH

from dependencies.meals.factories import MealQueryFactory
from domains.meals.events import InsertMealEvent, MealEvents
from taskiq import Context, TaskiqDepends
from pprint import pp


MODULE_PATH = (
    Path(__file__)
    .resolve()
    .relative_to(BASE_DIR_PATH)
    .with_suffix("")
    .as_posix()
    .replace("/", ".")
)


async def insert_meal(
    event: InsertMealEvent,
    context: Annotated[Context, TaskiqDepends()],
):
    event_type = context.state.events().get(MealEvents.INSERT)
    database = context.state.database
    query_factory = context.state.query_factories().get(
        MealQueryFactory.INSERT
    )
    validated_event = event_type.model_validate(event)
    query = query_factory.create(from_event=validated_event)

    await database.execute(query.statement, query.args)


class MealTasks(Enum):
    INSERT = f"{MODULE_PATH}:{insert_meal.__name__}"
