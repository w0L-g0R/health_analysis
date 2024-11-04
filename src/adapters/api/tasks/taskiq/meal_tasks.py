from dataclasses import dataclass
from enum import Enum
from typing import Union

from taskiq import AsyncTaskiqDecoratedTask

from src.adapters.spi.persistence.time_scale_db.meals.meals_repository import (
    MealsRepository,
)
from src.config.field_validator import FieldValidator
from src.ports.api.tasks.task import Task


class TaskiqTask(FieldValidator, Task):
    task: AsyncTaskiqDecoratedTask

    async def execute(self, data: str):
        print("Executing task", data)
        print("Task:", self.task)
        # if self.task is None:
        #     return

        t = await self.task.kiq(data=data)
        r = await t.wait_result(with_logs=True)

        return t, r


# class AddMealTask(TaskiqTask):
#     pass


# @dataclass
# class MealTasks(FieldValidator):
#     AddMealTask: AddMealTask
#     # add_one: Task


class MealTasks(Enum):
    ADD_MEAL = 1
