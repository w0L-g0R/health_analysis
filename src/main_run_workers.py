# import asyncio
# from multiprocessing import Process
# from pathlib import Path
# from time import sleep
#
# from taskiq.cli.worker.args import WorkerArgs
# from taskiq.cli.worker.run import run_worker
# from taskiq_aio_pika import AioPikaBroker
#
# SHELVE = []
#
# test_meals_broker = AioPikaBroker(
#     url="amqp://guest:guest@localhost:5672", queue_name="meals"
# )
#
# test_health_broker = AioPikaBroker(
#     url="amqp://guest:guest@localhost:5672", queue_name="health"
# )
#
#
# @test_meals_broker.task("add_meal_task_test")
# async def add_meal(meal: str, shelve: list) -> list:
#     print("SHELVE", meal)
#     shelve.append(meal)
#     # print(f"Adding meal: {MealTasks.query} + {meal}")
#     print(f"Shelve: {shelve}")
#
#     return shelve
#
#
# @test_health_broker.task("add_health_task")
# async def add_health(health: str) -> None:
#     print("Adding health: ", health)
#
#
# def start_meals_broker():
#     worker_args = WorkerArgs(
#         broker="src.main_run_workers:test_meals_broker",
#         modules=["src.main_run_workers"],
#     )
#
#     print("Meals broker is running")
#     run_worker(worker_args)
#
#
# def start_health_broker():
#     worker_args = WorkerArgs(
#         broker="src.main_run_workers:test_health_broker",
#         modules=["src.main_run_workers"],
#     )
#
#     print("Health broker is running")
#     run_worker(worker_args)
#
#
# async def start_tasks():
#     print("start_tasks")
#
#     await test_meals_broker.startup()
#     # await health_broker.startup()
#
#     add_meal_task_test = test_meals_broker.find_task(task_name="add_meal_task_test")
#     # add_health_task = health_broker.find_task(task_name="add_health_task")
#
#     # print(add_meal_task_test)
#     # print(add_health_task)
#     shelve = list()
#     while True:
#         t = await add_meal_task_test.kiq("Pizza", shelve)
#         res = await t.wait_result()
#         print(res)
#         # res = await add_health_task.kiq("Medipack")
#
#         await asyncio.sleep(5)
#
#
# if __name__ == "__main__":
#     p1 = Process(target=start_meals_broker)
#     p2 = Process(target=start_health_broker)
#
#     p1.start()
#     p2.start()
#
#     # p1.join()
#     # p2.join()
#
#     # sleep(2)
#     #
#     # print("Running main_run_workers.py")
#     #
#     # asyncio.run(start_tasks())
