from datetime import datetime, timezone
from enum import Enum

from taskiq_aio_pika import AioPikaBroker

from src.domains.meals.events import InsertMealEvent
from src.domains.meals.queries import InsertMealQuery


class InsertMealQueryFactory:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def create(self, from_event: InsertMealEvent) -> InsertMealQuery:
        return InsertMealQuery(
            time=datetime.now(tz=timezone.utc),
            meal_id=from_event.meal_id,
            user_id=from_event.user_id,
            meal_name=from_event.meal_name,
            calories=from_event.calories,
            table=self.table_name,
        )


class MealQueryFactory(Enum):
    INSERT = InsertMealQueryFactory.__name__
    # DELETE = "delete_meal_query"
