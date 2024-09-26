from uuid import UUID, uuid4

from pydantic import Field

from src.config.field_validator import FieldValidator


class MealDeleteEvent(FieldValidator):
    meal_id: UUID = Field(default_factory=uuid4)
    user_id: UUID = Field(default_factory=uuid4)

    class Config:
        frozen = True
