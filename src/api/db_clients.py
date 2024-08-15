from config import EVENTSTORE_DB_URL, TIMESCALE_DB_URL
from esdbclient import EventStoreDBClient
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

class EventStoreDb(EventStoreDBClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TimescaleDb:
    def __init__(self, connection):
        with psycopg2.connect(connection) as conn:
            cursor = conn.cursor()
            print(cursor)


event_store = EventStoreDb(uri=EVENTSTORE_DB_URL)
timescale_db = TimescaleDb(TIMESCALE_DB_URL)
