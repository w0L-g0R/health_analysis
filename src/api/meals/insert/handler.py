from datetime import datetime, timezone

from api.meals.insert.event import MealInsertEvent
from api.meals.insert.query import MealInsertQuery
from api.meals.repository import MealsRepository


class MealInsertEventHandler:
    def __init__(
        self,
        event_class: type[MealInsertEvent],
        repository: MealsRepository,
        query: MealInsertQuery,
    ):
        self.event_class = event_class
        self.repository = repository
        self.query = query

    async def process(self, event_data):
        print("HANDLER event_data: ", event_data)
        _ = self.event_class.model_validate(event_data)

        statement, args = self.query.insert_meal(
            time=datetime.now(timezone.utc),
            meal_id=_.meal_id,
            user_id=_.user_id,
            meal_name=_.meal_name,
            calories=_.calories,
        )

        await self.repository.execute(statement, args)
