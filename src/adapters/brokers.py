import asyncio
import subprocess
import sys
import logging
from typing import Callable, Dict
from aio_pika import ExchangeType
from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker

from src.config.config import get_module_path, setup_logging
from src.adapters.databases import TimeScaleDb
from src.adapters.exceptions.brokers import (
    BrokerRuntimeError,
    BrokerShutdownError,
    BrokerStartupError,
    InvalidExchangeNameError,
)


setup_logging()
logger = logging.getLogger(__name__)


class TaskiqBroker(AioPikaBroker):
    def __init__(
        self,
        url: str,
        name: str,
        tasks: Dict[str, Callable],
        database: TimeScaleDb,
        events: Dict,
        query_factories: Dict,
        exchange_name: str,
        queue_name: str,
    ):
        if not exchange_name:
            raise InvalidExchangeNameError()

        super().__init__(
            url=url,
            exchange_name=exchange_name,
            queue_name=queue_name,
            declare_exchange=True,
            declare_queues=True,
            kwargs={"durable": True},
        )
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
        database: TimeScaleDb,
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
        database: TimeScaleDb,
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
        process = None

        try:
            process = subprocess.Popen(cmd)
            process.wait()

        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received. Terminating the worker process.")
            if process:
                process.terminate()
                process.wait()

        except RuntimeError as re:
            logger.error(f"A runtime error occurred: {re}")
            if process:
                process.terminate()
                process.wait()
            raise BrokerRuntimeError(f"Runtime error in broker: {re}")

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            if process:
                process.terminate()
                process.wait()
            raise BrokerStartupError(f"Unexpected error in broker startup: {e}")

        finally:
            if process and process.poll() is None:
                logger.info("Shutting down the worker process.")
                process.terminate()
                process.wait()
                raise BrokerShutdownError("Error during broker shutdown.")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"""
                Broker with
                    name: {self.name}, 
                    id: {id(self)}, 
                    exchange_name: {self._exchange_name}, 
                    exchange_type: {self._exchange_type}, 
                    queue_name: {self._queue_name}, 
                    routing_key: {self._routing_key})"
                    tasks: {self.get_all_tasks()})"
                """
