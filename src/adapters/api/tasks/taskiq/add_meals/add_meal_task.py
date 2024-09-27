from typing import Callable, Union

from taskiq import AsyncTaskiqDecoratedTask

from src.adapters.spi.persistence.time_scale_db.meals.meals_repository import (
    MealsRepository,
)
from src.brokers.meals_broker import meals_broker
from src.config.field_validator import FieldValidator
from src.events.meals.add_meal_event import AddMealEvent
from src.models.meals.meal_model import Meal
from src.ports.api.tasks.task import Task


@meals_broker.task("add_one")
async def add_one():
    print("Adding one")


@meals_broker.task("add_meal_task")
async def add_meal_task(
    data: dict,
    event: Callable[..., AddMealEvent],
    # model: Callable[..., Meal],
    # repository: MealsRepository,
):
    try:
        dto = event.validate(data)
    except:
        print("errorir")

    print(dto)
    entity = Meal(
        meal_id=dto.meal_id,
        user_id=dto.user_id,
        data={
            "calories": dto.calories,
            "meal_name": dto.meal_name,
        },
    )

    query_args = entity.model_dump().values()
    print("query_args", query_args)

    # await repository.add_meal(tuple(query_args))


class AddMealTask(FieldValidator, Task):
    name: str
    repository: MealsRepository
    model: Callable[..., Meal]
    event: Callable[..., AddMealEvent]
    task: Union[None, AsyncTaskiqDecoratedTask] = None

    def set_task(self, task: AsyncTaskiqDecoratedTask):
        self.task = task

    async def execute(self, data: str):
        if self.task is None:
            return

        await self.task.kiq(data=data, event=self.event)


# class AddMealTask(FieldValidator, Task):
#     repo: MealsRepository
#     model: Callable[..., Meal]
#     add_meal_dto: AddMealDto
#
#     @meals_broker.task()
#     async def task(self, data: str):
#
#         dto = self.dto.model_validate(data)
#         entity = self.model(
#             meal_id=dto.meal_id,
#             user_id=dto.user_id,
#             data={
#                 "calories": dto.calories,
#                 "meal_name": dto.meal_name,
#             },
#         )
#
#         query_args = entity.model_dump().values()
#
#         await self.repo.add_meal(tuple(query_args))
#
#     async def execute(self, data: str):
#         await self.task.kiq(data)
