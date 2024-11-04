from taskiq import AsyncTaskiqDecoratedTask

from src.config.field_validator import FieldValidator
from src.interfaces.task import Task


class TaskiqTask(FieldValidator, Task):
    task: AsyncTaskiqDecoratedTask

    async def execute(self, data):
        print("Executing task", data)

        if self.task is None:
            print("No task assigned!", self.task)
            return

        await self.task.kiq(data=data)
