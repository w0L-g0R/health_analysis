# import asyncio
# import threading
#
#
# async def run_broker(broker: AioPikaBroker):
#     """Function to start the broker in an event loop."""
#     await broker.startup()
#     broker.register_task(func=task1, name="task1")
#
#     # Assume `start` is an async method that runs the broker
#
#
# def start_event_loop(loop, broker):
#     """Function to start an event loop in a separate thread."""
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(run_broker(broker))
#     loop.run_forever()
#
#
# def main():
#     # Create multiple event loops
#     loop1 = asyncio.new_event_loop()
#     loop2 = asyncio.new_event_loop()
#
#     # Assign event loops to different brokers
#     broker1 = AioPikaBroker(loop=loop1, url="amqp://guest:guest@localhost:5672")
#     broker2 = AioPikaBroker(loop=loop2, url="amqp://guest:guest@localhost:5672")
#
#     # Create threads to run event loops in parallel
#     thread1 = threading.Thread(target=start_event_loop, args=(loop1, broker1))
#     thread2 = threading.Thread(target=start_event_loop, args=(loop2, broker2))
#
#     try:
#         # Start the threads
#         thread1.start()
#         thread2.start()
#
#         print("Brokers are running in parallel. Press Ctrl+C to exit.")
#
#         tasks = broker1.get_all_tasks()
#         task = broker1.find_task(
#             task_name="C:.Users.Goritschnig.Wolfgang.Desktop.health_analysis.src.main:task1"
#         )
#         print(tasks)
#         print("task", task)
#
#         # Keep the main thread alive until KeyboardInterrupt
#         while True:
#
#             # t = await task.kiq()
#             # r = await t.wait_result()
#             pass
#
#     except KeyboardInterrupt:
#         print("Shutting down gracefully...")
#
#     finally:
#         # Close the event loops and threads
#         loop1.call_soon_threadsafe(loop1.stop)
#         loop2.call_soon_threadsafe(loop2.stop)
#
#         thread1.join()
#         thread2.join()
#
#         loop1.close()
#         loop2.close()
#
#         print("Event loops closed.")
#
#
# if __name__ == "__main__":
#     main()


# import asyncio
# import multiprocessing
#
# from taskiq_aio_pika import AioPikaBroker
#
#
# async def run_broker(broker: AioPikaBroker):
#     """Function to start the broker in its own event loop."""
#     await broker.startup()  # Assume `start` is an async method that runs the broker
#     await asyncio.Event().wait()  # Keep the loop alive indefinitely (until stopped)
#
#
# def process_target(broker_url):
#     """Target function to run a broker in a new process."""
#     broker = AioPikaBroker(url=broker_url)
#     asyncio.run(run_broker(broker))  # This runs the event loop automatically
#
#
# def main():
#     # Set up multiprocessing, one process per broker
#     process1 = multiprocessing.Process(
#         target=process_target, args=("amqp://guest:guest@localhost:5672",)
#     )
#
#     process2 = multiprocessing.Process(
#         target=process_target, args=("amqp://guest:guest@localhost:5673",)
#     )
#
#     try:
#         # Start the processes
#         process1.start()
#         process2.start()
#
#         print("Brokers are running in parallel. Press Ctrl+C to exit.")
#
#         # Keep the main process alive until KeyboardInterrupt
#         process1.join()
#         process2.join()
#
#     except KeyboardInterrupt:
#         print("Shutting down gracefully...")
#
#     finally:
#         # Terminate the processes if still alive
#         process1.terminate()
#         process2.terminate()
#
#         print("Processes terminated.")
#
#
# if __name__ == "__main__":
#     main()
