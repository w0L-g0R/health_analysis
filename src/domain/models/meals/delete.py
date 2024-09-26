from uuid import UUID

from src.config.validation import FieldValidator


class MealDeleteModel(FieldValidator):
    meal_id: UUID
    user_id: UUID

    class Config:
        frozen = True
