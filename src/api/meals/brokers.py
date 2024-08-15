from taskiq_redis import RedisAsyncResultBackend
from config import BROKER_URL, MEALS_QUEUE, TASK_RESULTS_URL
from taskiq_aio_pika import AioPikaBroker

meals_broker = AioPikaBroker(
    url=BROKER_URL, queue_name=MEALS_QUEUE
).with_result_backend(
    RedisAsyncResultBackend(
        redis_url=TASK_RESULTS_URL
    )
)
