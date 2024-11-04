from src.interfaces.queries import Queries


class MealsQueries(Queries):

    @staticmethod
    def add() -> str:
        return """
                INSERT INTO meals (meal_id, user_id, data) 
                VALUES ($1, $2, $3)
         """

    @staticmethod
    def delete() -> str:
        return """
                INSERT INTO meals (time, meal_id, user_id, meal_name, calories) 
                VALUES ($1, $2, $3, $4, $5)
         """
