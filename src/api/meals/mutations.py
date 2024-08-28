from datetime import datetime, timezone
from typing import Callable, Tuple
from uuid import UUID

from api.meals.models import Meal

InsertMealArgs = Tuple[str, UUID, UUID, str, float]
InsertMealReturn = Tuple[str, InsertMealArgs]
InsertMeal = Callable[[Meal], Tuple[str, InsertMealArgs]]


class MealMutations:
    @staticmethod
    def insert_meal(meal: Meal) -> InsertMealReturn:
        time = datetime.now(timezone.utc).isoformat()
        args = (
            time,
            str(meal.meal_id),
            str(meal.user_id),
            str(meal.meal_name),
            str(meal.calories),
        )

        statment = """INSERT INTO meals (time, meal_id, user_id, meal_name, calories) VALUES (%s, %s, %s, %s, %s);"""

        return (statment, args)
