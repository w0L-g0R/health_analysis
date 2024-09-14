from datetime import datetime, timezone
from typing import Callable
from domain.meals.events import (
    InsertMealEvent,
)
from domain.meals.queries import InsertMealQuery


# util that wraps the table name from the config to the query
def insert_meal_query_factory(
    table_name: str,
) -> Callable[[InsertMealEvent], InsertMealQuery]:
    def factory(
        from_event: InsertMealEvent,
    ) -> InsertMealQuery:
        return InsertMealQuery(
            time=datetime.now(tz=timezone.utc),
            meal_id=from_event.meal_id,
            user_id=from_event.user_id,
            meal_name=from_event.meal_name,
            calories=from_event.calories,
            table_name=table_name,
        )

    return factory
