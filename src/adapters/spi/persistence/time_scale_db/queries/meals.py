from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel


class MealsQueries(BaseModel):
    INSERT: str = (
        """INSERT INTO meals (time, meal_id, user_id, meal_name, calories) VALUES ($1, $2, $3, $4, $5)"""
    )

    DELETE: str = """DELETE FROM meals WHERE meal_id = $1 AND user_id = $2"""
