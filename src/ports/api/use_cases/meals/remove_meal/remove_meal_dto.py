from uuid import UUID
from pydantic import Field
from src.config.field_validator import FieldValidator


class RemoveMealDto(FieldValidator):
    meal_id: UUID
    user_id: UUID

    class Config:
        frozen = True
