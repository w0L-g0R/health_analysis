import json
from typing import Annotated

from taskiq import Context, TaskiqDepends

from src.brokers.meals_broker import meals_broker
from src.events.meals.add_meal_event import AddMealEvent


@meals_broker.task("health_check")
async def meal_broker_health_check(x):
    pass


@meals_broker.task(AddMealEvent.__name__)
async def add_meal_task(
    data: str,
    context: Annotated[Context, TaskiqDepends()],
):

    data = context.state.validators[AddMealEvent.__name__].parse_raw(data)

    meal_data = json.dumps(
        {
            "calories": data.calories,
            "meal_name": data.meal_name,
        }
    )

    entity = context.state.model()(
        meal_id=data.meal_id, user_id=data.user_id, meal_data=meal_data
    )

    query_args = list(entity.model_dump().values())

    result = await context.state.repository.add(query_args)

    print("Result:", result)
