import asyncio
import json

from taskiq import InMemoryBroker
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from api.meals.brokers import meals_broker as broker
# from api.health.brokers import health_broker 
from api.db_clients import event_store

# from taskiq.api import run_receiver_task
from pprint import PrettyPrinter as printer

from api.meals.meals import Meal
from api.meals.tasks import add_meal
from taskiq.api import run_receiver_task

from config import BROKER_URL, HEALTH_QUEUE, MEALS_QUEUE, TASK_RESULTS_URL

async def main() -> None:

    try:
        await broker.startup()
        while True:

            # broker.register_task(
            #     lambda x: add_meal(x),
            #     task_name="add_meal",
            #     my_label=1
            # )


            print("broker.get_all_tasks(): ", broker.get_all_tasks())
            # print("meals_broker.get_all_tasks(): ", meals_broker.get_all_tasks())
            stream_name = "meals_added"
            catchup_subscription = event_store.subscribe_to_stream(
                stream_name=stream_name, from_end=True
            )
            for event in catchup_subscription:
                # printer(indent=2).pprint(event.data)
                printer(indent=2).pprint(type(event))

                # if (event):
                #     eventdata = json.loads(event.decode('utf-8'))
                #     event.
                #     printer(indent=2).pprint(eventdata)

                if event.data:
                    print("event.type : ", event.type)
                    try:
                        if event.type == "Meals":
                            
                            # await health_broker.startup()
                            # worker_task = asyncio.create_task(run_receiver_task(meals_broker))
                            mealdata = Meal.model_validate_json(event.data)
                            print("meal_name: ", mealdata.meal_name)

                            meals_broker = AioPikaBroker(
                                url=BROKER_URL, queue_name=HEALTH_QUEUE_QUEUE
                            ).with_result_backend(
                                RedisAsyncResultBackend(
                                    redis_url=TASK_RESULTS_URL
                                )
                            )


                            # add_meal_task = await add_one.kiq(int(mealdata.calories))
                            print('broker._queue_name: ', broker._queue_name)
                            broker._queue_name = "justa_queue"
                            print('broker._queue_name: ', broker._queue_name)
                            
                            add_meal_task = await add_meal.kicker().kiq(mealdata.meal_name)
                            
                            print("add_meal_task: ", add_meal_task.task_id)
                            p = await add_meal_task.get_progress()
                            print('add_meal_task.p: ',p )

                            result = await add_meal_task.wait_result(timeout=2,with_logs=True)
                            
                            print(result.log)

                            print(
                                f"Task execution took: {result.execution_time} seconds."
                            )

                            if result.is_err:
                                print("Error found while executing task.\n")

                            print(f"Returned value: {result.return_value}\n")

                            # worker_task.cancel()
                            
                            # try:
                            #     await worker_task
                            # except asyncio.CancelledError:
                            #     print("Worker successfully exited.")
                                
                    except Exception as e:
                            print(e)
                                
                    # printer(indent=2).pprint(mealdata)

                    # 1 kick calculation function with data

                # if (event.metadata):
                #     print(event.metadata)
                #     printer(indent=2).pprint(event.metadata)

                # printer(event.data)
                # serializer = MealsSerializer(data=data)

                # Validate the data
                # if serializer.is_valid():
                #     # If valid, save the new instance
                #     meal_instance = serializer.save()
                #     # send_to_analysis(event.data)
                #     print("Meal instance created:", meal_instance)
                # else:
                #     # If not valid, print the errors
                #     print("Validation errors:", serializer.errors)

                # client.stub.AddMeal()

            # add_meals("Bread and butter")
            # Meals.objects.create(user_id=uuid.uuid4(), meal_id=uuid.uuid4(), meal_name=fake.name(), calories=fake.random_digit_not_null())
            print("Finished event listening")

    except KeyboardInterrupt:
        catchup_subscription.stop()
        await health_broker.shutdown()
        await broker.shutdown()
        print("Task repetition stopped.")

    return


# async def main() -> None:
# Here we define a broker.
# worker_task = asyncio.create_task(run_receiver_task(broker))

# Now we register lambda as a task.
# broker.register_task(
#     lambda x: add_meal(x),
#     task_name="add_meal",
#     my_label=1
# )

# found = broker.find_task("add_meal")
# print('found: ', found)
# Now we can send it.


# await found.kiq(x=1)

# await asyncio.sleep(2)

# # worker_task.cancel()
# try:
#     await worker_task
# except asyncio.CancelledError:
#     print("Worker successfully exited.")

# await broker.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
