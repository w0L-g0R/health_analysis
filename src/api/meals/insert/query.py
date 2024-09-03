from dataclasses import dataclass
import datetime
from uuid import uuid4


@dataclass
class MealInsertQuery:
    @staticmethod
    def insert_meal(
        time: datetime, meal_id: uuid4, user_id: uuid4, meal_name: str, calories: float
    ):
        statement = """
            INSERT INTO public.meals (time, meal_id, user_id, meal_name, calories)
            VALUES ($1, $2, $3, $4, $5)
        """

        args = (time, meal_id, user_id, meal_name, calories)

        return statement, args
