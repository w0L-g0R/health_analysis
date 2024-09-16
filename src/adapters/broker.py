import asyncio
import subprocess
import sys
from typing import Callable, Dict
from taskiq import AsyncBroker, TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker

from src.adapters.database import Database
from dependency_injector.providers import (
    Resource,
)

import logging

from src.config import get_module_path, setup_logging


setup_logging()
logger = logging.getLogger(__name__)


class Broker(AioPikaBroker):
    def __init__(
        self,
        url,
        name: str,
        tasks: Dict[str, Callable],
        database,
        events: Dict,
        query_factories: Dict,
    ):
        super().__init__(url)
        self.name = name
        self.register_tasks(tasks)
        self.add_event_handlers(
            database,
            events,
            query_factories,
        )

    def register_tasks(self, tasks: Dict[str, Callable]):
        for task_name, task_func in tasks.items():
            self.register_task(
                func=task_func,
                name=task_name,
            )

    def add_event_handlers(
        self,
        database,
        events: Dict,
        query_factories: Dict,
    ):
        self.add_event_handler(
            event=TaskiqEvents.WORKER_STARTUP,
            handler=lambda state: self.handle_startup_worker_event(
                state=state,
                database=database,
                events=events,
                query_factories=query_factories,
            ),
        )

        self.add_event_handler(
            event=TaskiqEvents.WORKER_SHUTDOWN,
            handler=lambda state: self.handle_shutdown_worker_event(
                state=state,
            ),
        )

        pass

    async def handle_startup_worker_event(
        self,
        state: TaskiqState,
        database,
        events: Dict,
        query_factories: Dict,
    ):
        state.database = await database
        state.events = events
        state.query_factories = query_factories

    async def handle_shutdown_worker_event(self, state: TaskiqState):
        try:
            if not asyncio.get_event_loop().is_closed():
                logger.info("Shutting down the database.")
                await state.database.close()

        except RuntimeError as e:
            if str(e) == "Event loop is closed":
                logger.error(
                    "Event loop is closed, but still trying to close the database connection."
                )
            else:
                logger.error(f"RuntimeError during shutdown: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during shutdown: {e}")

        finally:
            await state.database.close()

    def start_workers_process(self, file: str):
        cmd = [
            sys.executable,
            "-m",
            "taskiq",
            "worker",
            f"{get_module_path(file)}:{self.name}",
        ]
        return subprocess.Popen(cmd)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Broker(name={self.name})"
