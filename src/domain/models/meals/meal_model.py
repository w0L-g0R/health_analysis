from uuid import UUID
from pydantic import Field
from src.config.field_validator import FieldValidator


class Meal(FieldValidator):
    meal_id: UUID
    user_id: UUID
    meal_name: str = Field(min_length=3)
    calories: float = Field(gt=0)

    class Config:
        frozen = True
