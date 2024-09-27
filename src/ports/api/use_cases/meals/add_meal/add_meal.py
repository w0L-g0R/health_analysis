from uuid import UUID, uuid4
from pydantic import Field
from src.config.field_validator import FieldValidator


class AddMealDto(FieldValidator):
    meal_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    meal_name: str = Field(min_length=3)
    calories: float = Field(gt=0)

    class Config:
        frozen = True
