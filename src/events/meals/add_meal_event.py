from typing import Any, Self
from uuid import UUID
from pydantic import Field, UUID4
from src.config.field_validator import FieldValidator


class AddMealEvent(FieldValidator):
    meal_id: UUID4
    user_id: UUID4
    meal_name: str = Field(min_length=3)
    calories: float = Field(gt=0)

    @staticmethod
    def validate(data: dict):
        return AddMealEvent.model_validate(data)

    class Config:
        frozen = True
