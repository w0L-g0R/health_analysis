from dotenv import load_dotenv
import os

load_dotenv()

TIMESCALE_DB_URL = os.getenv('TIMESCALE_DB_URL')
EVENTSTORE_DB_URL = os.getenv('EVENTSTORE_DB_URL')
BROKER_URL = os.getenv('BROKER_URL')
TASK_RESULTS_URL = os.getenv('TASK_RESULTS_URL')

MEALS_QUEUE = os.getenv('TASK_RESULTS_URL')
HEALTH_QUEUE = os.getenv('TASK_RESULTS_URL')


# print(CONNECTION)


# with psycopg2.connect(CONNECTION) eas conn:
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM etl_meals")
#     print(cursor.fetchone())