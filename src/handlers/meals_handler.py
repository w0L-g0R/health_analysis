# from taskiq_aio_pika import AioPikaBroker

# from src.abstractions.handler import EventHandler
# from src.tasks.meal_tasks import MealTasks


from src.tasks.meal_tasks import MealsTasks


class MealsHandler:
    ##
    def __init__(self, tasks):
        self.tasks = tasks

    async def handle(self, event):
        match event.type:
            case MealsTasks.insert_meal.__name__:
                print("case MealsTasks.insert_meal.__name__:: ")

                # await MealsTasks.insert_meal(event)
                # await insert_event_handler.validate_and_serialize(event)
                # insert_event_handler.process(event.data.decode("utf-8"))
                # process_insert_meal_event.send(
                #     event.data.decode("utf-8"),
                # )
                pass
                # process(event.data.decode("utf-8"))
            case _:
                print("No matching type")

        pass
        # task = meals_broker.find_task(task_name=MealTasks.INSERT.value)

        # if task:
        #     _task = await task.kiq(event_insert_meal)
        #     # _task2 = await task.kiq("event2")
        #     res = await _task.wait_result()
        #     # res2 = await _task2.wait_result()
        #     print("res: ", res)
        #     # print("res2: ", res2)
