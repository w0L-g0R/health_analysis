from api.handlers import (
    shutdown_worker_event_handler,
    startup_worker_event_handler,
)

from domain.meals.tasks import MealTasks, insert_meal
from taskiq import TaskiqEvents

from dependencies.bootstrap import (
    meals_container as container,
)

broker = container.broker()


broker.register_task(
    func=insert_meal,
    name=MealTasks.INSERT.value,
)

broker.add_event_handler(
    event=TaskiqEvents.WORKER_STARTUP,
    handler=lambda state: startup_worker_event_handler(
        state=state,
        database=container.database,
        events=container.events,
        queries=container.queries,
    ),
)

broker.add_event_handler(
    event=TaskiqEvents.WORKER_SHUTDOWN,
    handler=lambda state: shutdown_worker_event_handler(
        state=state, database=container.database
    ),
)
