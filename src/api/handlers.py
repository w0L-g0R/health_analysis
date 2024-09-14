import asyncio
from dependency_injector.providers import Resource, Dict
import logging

from dependencies.infrastructure.database import (
    TimeScaleDatabase,
)
from taskiq import TaskiqState


async def startup_worker_event_handler(
    state: TaskiqState,
    database: Resource[TimeScaleDatabase],
    events: Dict,
    queries: Dict,
):
    state.database = await database()
    state.events = events
    state.queries = queries


async def shutdown_worker_event_handler(
    state: TaskiqState, database: Resource[TimeScaleDatabase]
):
    try:
        if not asyncio.get_event_loop().is_closed():
            logging.info("Shutting down the database.")
            await state.database.close()

    except RuntimeError as e:
        if str(e) == "Event loop is closed":
            logging.error(
                "Event loop is closed, but still trying to close the database connection."
            )
        else:
            logging.error(
                f"RuntimeError during shutdown: {e}"
            )
    except Exception as e:
        logging.error(
            f"Unexpected error during shutdown: {e}"
        )
    finally:
        await state.database.close()
