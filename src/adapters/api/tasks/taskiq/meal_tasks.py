from taskiq import AsyncTaskiqDecoratedTask

from src.adapters.api.tasks.taskiq.add_meals.add_meal_task import AddMealTask
from src.config.field_validator import FieldValidator
from src.ports.api.tasks.task import Task


class MealTasks(FieldValidator):
    add_meal: AddMealTask
    # add_one: Task
