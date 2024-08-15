from api.health.brokers import health_broker

@health_broker.task(task_name="add_health", queue_name="health_queue")
def add_health(health: str) -> str:
    return health
