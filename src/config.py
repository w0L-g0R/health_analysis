import os

from dotenv import load_dotenv

load_dotenv()

TIMESCALE_DB = os.getenv("TIMESCALE_DB")
EVENTSTORE = os.getenv("EVENTSTORE")
RABBIT_MQ = os.getenv("RABBIT_MQ")
REDIS_RESULTS = os.getenv("REDIS_RESULTS")

MEALS_QUEUE = os.getenv("MEALS_QUEUE")
HEALTH_QUEUE = os.getenv("HEALTH_QUEUE")

MEALS_TABLE = os.getenv("MEALS_TABLE")
HEALTH_TABLE = os.getenv("HEALTH_TABLE")
