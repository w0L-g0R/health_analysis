from uuid import UUID

from src.config.field_validator import FieldValidator


class MealDeleteModel(FieldValidator):
    meal_id: UUID
    user_id: UUID

    class Config:
        frozen = True
