# import asyncio
import asyncio
from enum import Enum
from pathlib import Path
from typing import Annotated

from domain.meals.events import InsertMealEvent, MealEvents
from domain.meals.queries import MealQueries
from taskiq import Context, TaskiqDepends
from pprint import pp


async def insert_meal(
    event: InsertMealEvent,
    context: Annotated[Context, TaskiqDepends()],
):
    pp(context.state, indent=2, sort_dicts=True, depth=4)

    event_type = context.state.events().get(MealEvents.INSERT)

    database = context.state.database

    query_factory = context.state.queries().get(
        MealQueries.INSERT
    )
    print("query_factory: ", query_factory)

    validated_event = event_type.model_validate(event)

    print("validated_event: ", validated_event)

    query = query_factory(from_event=validated_event)

    print("query: ", query)

    query2 = query_factory(from_event=validated_event)

    print("query2: ", query2)

    await database.execute(query.statement, query.args)

    await asyncio.sleep(0.1)


BASE_DIR_PATH = Path.cwd() / "src"


MODULE_PATH = (
    Path(__file__)
    .resolve()
    .relative_to(BASE_DIR_PATH)
    .with_suffix("")
    .as_posix()
    .replace("/", ".")
)


class MealTasks(Enum):
    INSERT = f"{MODULE_PATH}:{insert_meal.__name__}"
