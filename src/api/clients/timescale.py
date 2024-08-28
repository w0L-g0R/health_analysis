from typing import Optional

from psycopg2 import DatabaseError, Error, connect, sql
from psycopg2.extensions import connection

from api.meals.mutations import InsertMealArgs


class TimescaleDbClient:
    def close(self) -> None:
        self.connection.close()

    def __init__(self, connection: connection):
        try:
            connect(connection)
            self.connection = connection

        except Error as e:
            print(f"Connection error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def execute(
        self, sql: sql.SQL, args: InsertMealArgs
    ) -> Optional[str]:
        try:
            with connect(self.connection) as conn:
                conn.cursor().execute(sql, args)
                conn.commit()

        except (Exception, DatabaseError, Error) as error:
            print(error)
