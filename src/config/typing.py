import logging
from typing import TypedDict, Dict, Callable
from logging import StreamHandler


class TimeScaleDbTables(TypedDict):
    meals: str


class TimeScaleDb(TypedDict):
    dsn: str
    user: str
    password: str
    host: str
    port: str
    database: str
    tables: TimeScaleDbTables


class EventStoreDb(TypedDict):
    uri: str


class Redis(TypedDict):
    uri: str


class RabbitMq(TypedDict):
    url: str
    user: str
    password: str
    host: str
    port: str
    meals: Dict[str, str]


class Dsn(TypedDict):
    timescaledb: TimeScaleDb
    eventstoredb: EventStoreDb
    redis: Redis
    rabbitmq: RabbitMq


class Subscriptions(TypedDict):
    stream: str
    from_end: bool


class Events(TypedDict):
    insert: str


class Formatter(TypedDict):
    format: str


class ConsoleHandler(TypedDict):
    class_: logging.Handler
    level: str
    formatter: str
    stream: str


class Handlers(TypedDict):
    console: ConsoleHandler


class Logging(TypedDict):
    version: int
    formatters: Dict[str, Formatter]
    handlers: Handlers
    root: Dict[str, str]


class Config(TypedDict):
    dsn: Dsn
    rabbitmq: Dict[str, Dict[str, str]]
    subscriptions: Dict[str, Subscriptions]
    events: Dict[str, Events]
    logging: Logging
