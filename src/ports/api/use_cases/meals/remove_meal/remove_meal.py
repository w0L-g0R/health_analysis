from uuid import UUID
from pydantic import Field
from src.config.field_validator import FieldValidator


class RemoveMealDto(FieldValidator):
    meal_id: UUID = Field(default_factory=UUID)
    user_id: UUID = Field(default_factory=UUID)

    class Config:
        frozen = True
