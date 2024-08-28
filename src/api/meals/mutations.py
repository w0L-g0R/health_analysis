from dataclasses import dataclass
from typing import Callable, Tuple
from uuid import UUID

from api.meals.models import Meal


@dataclass
class MealMutations:
    insert_statement: str = """
        INSERT INTO meals 
        (time, meal_id, user_id, meal_name, calories) 
        VALUES (%s, %s, %s, %s, %s);
        """
