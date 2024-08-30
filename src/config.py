import os

import psycopg2
from dotenv import load_dotenv

path = os.path.join(os.getcwd(), "pg_service.conf")

print("path: ", path)

os.environ["PGSERVICEFILE"] = path

load_dotenv()

TIMESCALE_DB = os.getenv("TIMESCALE_DB")
EVENTSTORE = os.getenv("EVENTSTORE")
RABBIT_MQ = os.getenv("RABBIT_MQ")
REDIS_RESULTS = os.getenv("REDIS_RESULTS")

MEALS_QUEUE = os.getenv("MEALS_QUEUE")
HEALTH_QUEUE = os.getenv("HEALTH_QUEUE")

MEALS_TABLE = os.getenv("MEALS_TABLE")
HEALTH_TABLE = os.getenv("HEALTH_TABLE")



