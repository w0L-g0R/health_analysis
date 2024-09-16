# from taskiq_aio_pika import AioPikaBroker

# from src.abstractions.handler import EventHandler
# from src.tasks.meal_tasks import MealTasks


# class MealsHandler(EventHandler):
#     ##
#     @staticmethod
#     async def handle(broker: AioPikaBroker):
#         task = meals_broker.find_task(task_name=MealTasks.INSERT.value)

#         if task:
#             _task = await task.kiq(event_insert_meal)
#             # _task2 = await task.kiq("event2")
#             res = await _task.wait_result()
#             # res2 = await _task2.wait_result()
#             print("res: ", res)
#             # print("res2: ", res2)
