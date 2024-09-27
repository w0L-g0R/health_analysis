from abc import ABC
from typing import Protocol

from src.domain.models.meals.meal_results import MealMutationResult
from src.ports.api.use_cases.meals.add_meal.add_meal import AddMeal


class AddMealUseCase(ABC):
    async def add_meal(self, dto: str) -> MealMutationResult:
        raise NotImplementedError()
