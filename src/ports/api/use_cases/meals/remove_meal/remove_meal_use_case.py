from src.domain.models.meals.meal_results import MealMutationResult
from abc import ABC


class RemoveMealUseCase(ABC):
    async def remove_meal(self, dto: str) -> MealMutationResult:
        raise NotImplementedError()
