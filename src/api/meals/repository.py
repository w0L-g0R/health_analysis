import logging


class MealsRepository:
    def __init__(self, pool):
        self.pool = pool

    def execute(self, statement, data):
        connection = None
        try:
            # Acquire a connection from the pool
            connection = self.pool.getconn()
            cursor = connection.cursor()

            # Execute the query
            cursor.execute(statement, data)

            # Commit the transaction
            connection.commit()
            cursor.close()

        except Exception as e:
            if connection:
                connection.rollback()
            logging.error(f"Error executing query: {e}")

        finally:
            # Return the connection back to the pool
            if connection:
                self.pool.putconn(connection)

    def close(self):
        # Close all connections in the pool
        if self.pool:
            self.pool.closeall()
            logging.info(
                "Closed all connections in the pool."
            )


# class MealsRepository:
#     def __init__(self, pool: ThreadedConnectionPool):
#         self.pool = pool
#         if pool:
#             logging.info(
#                 f"Initialized meals repository {id(self)} with pool {id(self.pool)}",
#             )

#     def execute(self, statement: str, args: tuple):
#         try:
#             with self.pool.getconn() as connection:
#                 with connection.cursor() as cursor:
#                     cursor.execute(statement, *args)

#         except Exception as e:
#             logging.error(e)

#     async def close(self):
#         if self.pool:
#             self.pool.allclose()
#             logging.info(
#                 f"Closed meals repository {id(self)} with pool {id(self.pool)}: {self.pool._closed}",
#             )
