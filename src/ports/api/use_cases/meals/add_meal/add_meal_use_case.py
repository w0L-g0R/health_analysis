from abc import ABC

from src.domain.models.meals.meal_results import MealMutationResult


class AddMealUseCase(ABC):
    async def add_meal(self, dto: str) -> MealMutationResult:
        raise NotImplementedError()
