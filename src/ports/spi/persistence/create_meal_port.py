from abc import ABC
from src.domain.models.meals.meal_model import Meal


class CreateMealPort(ABC):
    def create_meal(self, *args) -> Meal:
        raise NotImplementedError()
