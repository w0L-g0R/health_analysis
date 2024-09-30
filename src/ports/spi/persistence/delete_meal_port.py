from abc import ABC
from uuid import UUID

from src.domain.models.meals.meal_model import Meal


class DeleteMealPort(ABC):
    def execute(self, meal_id: UUID, user_id: UUID) -> Meal:
        raise NotImplementedError()
