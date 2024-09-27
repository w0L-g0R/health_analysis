from typing import Protocol
from src.domain.models.meals.meal_results import MealMutationResult
from src.ports.api.use_cases.meals.remove_meal.remove_meal import RemoveMealDto


class RemoveMealUseCase(Protocol):
    async def remove_meal(self, dto: str) -> MealMutationResult:
        raise NotImplementedError()
