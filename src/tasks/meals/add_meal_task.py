from typing import Callable

from src.config.field_validator import FieldValidator
from src.domain.models.meals.meal_model import Meal
from src.ports.api.use_cases.meals.add_meal.add_meal_dto import AddMealDto
from src.ports.spi.persistence.create_meal_port import CreateMealPort

from src.ports.api.use_cases.meals.add_meal.add_meal_use_case import AddMealUseCase


class AddMealTask(FieldValidator, AddMealUseCase):
    create_meal: CreateMealPort
    model: Callable[..., Meal]
    add_meal_dto: AddMealDto

    async def add_meal(self, data: str):
        dto = self.dto.model_validate(data)
        entity = self.model(
            meal_id=dto.meal_id,
            user_id=dto.user_id,
            data={
                "calories": dto.calories,
                "meal_name": dto.meal_name,
            },
        )

        query_args = entity.model_dump().values()

        await self.create_meal.execute(tuple(query_args))
