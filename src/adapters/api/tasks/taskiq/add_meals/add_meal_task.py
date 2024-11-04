import asyncio
import random
from typing import Annotated, Union

from dependency_injector.providers import Callable
from taskiq import AsyncTaskiqDecoratedTask, Context, TaskiqDepends

from src.adapters.api.tasks.taskiq.meal_tasks import MealTasks
from src.adapters.spi.persistence.time_scale_db.meals.meals_repository import (
    MealsRepository,
)
from src.brokers.meals_broker import meals_broker
from src.config.field_validator import FieldValidator

# from src.brokers.meals_broker import meals_broker
from src.containers.meals_container import MealsContainer
from src.events.meals.add_meal_event import AddMealEvent


# def common_dep() -> int:
#     return random.randint(1, 10)
#


@meals_broker.task("add_one")
async def add_one(
    data: str,
    # con: Annotated[int, TaskiqDepends(common_dep)],
    # container: Annotated[MealsContainer, TaskiqDepends()],
):
    print("Adding one:", data)
    # print("Adding con:", con)
    # print("Container:", container.repository)


@meals_broker.task(str(MealTasks.ADD_MEAL))
async def add_meal_task(
    data: str,
    context: Annotated[Context, TaskiqDepends()],
):
    print("ffa", data)
    print("context", context)
    # return "yes"
    # print("Data", data)
    # print("context repo", context.state.repository)
    #
    # validator = context.state.validators[AddMealEvent.__name__]
    # model = context.state.model()
    # print("event_data_validator", validator)
    #
    # try:
    #     data = validator.validate(data)
    # except:
    #     print("error validating event data")
    #
    # print("event_data_validator", validator)
    # print("model", model)

    # try:
    #     dto = event.validate(data)
    # except:
    #     print("errorir")
    #
    # print(dto)
    # entity = Meal(
    #     meal_id=dto.meal_id,
    #     user_id=dto.user_id,
    #     data={
    #         "calories": dto.calories,
    #         "meal_name": dto.meal_name,
    #     },
    # )
    #
    # query_args = entity.model_dump().values()
    # print("query_args", query_args)
    # await asyncio.sleep(1)

    # await repository.add_meal(tuple(query_args))


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
