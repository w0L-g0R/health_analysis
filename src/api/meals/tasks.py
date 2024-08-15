from api.meals.brokers import meals_broker

@meals_broker.task(task_name="add_meal", queue_name="meals_queue")
def add_meal(meal: str) -> str:
    return meal
