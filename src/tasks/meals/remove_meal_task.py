from typing import Callable

from pydantic import validate_call

from src.config.field_validator import FieldValidator
from src.domain.models.meals.meal_model import Meal
from src.ports.api.use_cases.meals.remove_meal.remove_meal_dto import RemoveMealDto
from src.ports.api.use_cases.meals.remove_meal.remove_meal_use_case import (
    RemoveMealUseCase,
)
from src.ports.spi.persistence.delete_meal_port import DeleteMealPort


class RemoveMealTask(
    FieldValidator,
    RemoveMealUseCase,
):
    delete_meal: DeleteMealPort
    model: Callable[..., Meal]
    add_meal_dto: RemoveMealDto

    @validate_call
    async def delete_meal(self, data: str):
        dto = self.dto.model_validate(data)

        entity = self.model(
            meal_id=dto.meal_id,
            user_id=dto.user_id,
        )

        query_args = entity.model_dump().values()

        await self.delete_meal.execute(tuple(query_args))
