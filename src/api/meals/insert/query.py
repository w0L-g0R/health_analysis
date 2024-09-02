from dataclasses import dataclass
from typing import Tuple


@dataclass
class MealInsertQuery:
    @staticmethod
    def insert(args: Tuple[str, str, str, str, str]):
        statement = """
            INSERT INTO meals (time, meal_id, user_id, meal_name, calories)
            VALUES ($1, $2, $3, $4, $5)
        """

        return (statement, args)
