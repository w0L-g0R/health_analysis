from uuid import uuid4
from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker


broker = AioPikaBroker(url="amqp://guest:guest@127.0.0.1:5672")

shared_db = None  # To hold the shared DB pool


def get_db():
    global shared_db
    if shared_db is None:
        # Initialize the shared resource (e.g., pool or UUID) only once
        shared_db = uuid4()  # or `await asyncpg.create_pool(...)`
    return shared_db


# Inject the same shared db into each worker's context
@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    db = get_db()  # The same shared resource
    broker.add_dependency_context({"database": db})
    print("Shared db: ", db)
    state.db = db
