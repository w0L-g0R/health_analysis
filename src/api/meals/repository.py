import logging

from psycopg2.pool import SimpleConnectionPool

# from psycopg2.errors.


class MealsRepository:
    insert_statement = """
            INSERT INTO meals 
                (time, meal_id, user_id, meal_name, calories) 
                    VALUES (%s, %s, %s, %s, %s);
            """

    def __init__(self, pool: SimpleConnectionPool):
        self.pool = pool
        if pool:
            logging.info(
                f"Initialized meals repository {id(self)} with pool {id(self.pool)}",
            )

    def execute(self, statement, **args):
        try:
            with self.pool.getconn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(statement, args)

        # except DataBaseError as e:
        #     logging.error(e)

        except Exception as e:
            logging.error(e)

        finally:
            conn.close()

    def close(self):
        if self.pool:
            self.pool.closeall()
            logging.info(
                f"Closed meals repository {id(self)} with pool {id(self.pool)}: {self.pool.closed}",
            )
