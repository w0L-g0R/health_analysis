from uuid import UUID
from pydantic import Field
from src.config.field_validator import FieldValidator


class Meal(FieldValidator):
    meal_id: UUID
    user_id: UUID
    data: dict = Field(default=None)

    class Config:
        frozen = True
