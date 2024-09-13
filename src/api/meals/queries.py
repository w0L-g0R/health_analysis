from datetime import datetime
from uuid import UUID, uuid4


class MealInsertQueries:
    @staticmethod
    def insert_meal(
        time: datetime, meal_id: UUID, user_id: UUID, meal_name: str, calories: float
    ):
        statement = """
            INSERT INTO public.meals (time, meal_id, user_id, meal_name, calories)
            VALUES ($1, $2, $3, $4, $5)
        """

        args = (time, meal_id, user_id, meal_name, calories)

        return statement, args
