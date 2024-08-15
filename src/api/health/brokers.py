from taskiq_redis import RedisAsyncResultBackend
from config import BROKER_URL, HEALTH_QUEUE, TASK_RESULTS_URL
from taskiq import InMemoryBroker
from taskiq_aio_pika import AioPikaBroker

# health_broker = AioPikaBroker(
#     url=BROKER_URL, queue_name=HEALTH_QUEUE
# ).with_result_backend(
#     RedisAsyncResultBackend(
#         redis_url=TASK_RESULTS_URL, result_ex_time=100000
#     )
# )
