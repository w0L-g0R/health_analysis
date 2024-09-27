from typing import Protocol
from uuid import UUID

from src.domain.models.meals.meal_model import Meal


class DeleteMealPort(Protocol):
    def delete_meal(self, meal_id: UUID, user_id: UUID) -> Meal:
        raise NotImplementedError()
